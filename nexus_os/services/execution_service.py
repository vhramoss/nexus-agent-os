import asyncio
import builtins
import hashlib
import time
from concurrent.futures import ProcessPoolExecutor

from fastapi import HTTPException

from nexus_os.core.agents.orchestrator.agent import NexusAgent
from nexus_os.core.contracts.agent import AgentInput
from nexus_os.core.runtime.dead_letter_queue import DeadLetterQueue
from nexus_os.core.runtime.execution_context import ExecutionContext
from nexus_os.core.runtime.execution_store import ExecutionStore
from nexus_os.core.runtime.queue_gate import QueueGate
from nexus_os.core.runtime.redis_dead_letter_queue import RedisDeadLetterQueue
from nexus_os.core.runtime.redis_queue_gate import RedisQueueGate
from nexus_os.core.runtime.supervisor import Supervisor
from nexus_os.core.runtime.user_queue_gate import UserQueueGate
from nexus_os.infra.config import get_settings

# -----------------------------
# Config
# -----------------------------

settings = get_settings()

max_concurrent = settings.max_concurrent
execution_timeout = settings.exec_timeout
use_redis = settings.use_redis
redis_url = settings.redis_url

# -----------------------------
# Runtime
# -----------------------------

process_pool = ProcessPoolExecutor(max_workers=max_concurrent)
supervisor = Supervisor()
user_queue_gate = UserQueueGate(max_per_user=2)
store = ExecutionStore()

event_bus = None

if use_redis:
    queue_gate = RedisQueueGate(redis_url=redis_url, max_concurrent=max_concurrent)
    dead_letter_queue = RedisDeadLetterQueue(redis_url=redis_url)
else:
    queue_gate = QueueGate(max_concurrent=max_concurrent)
    dead_letter_queue = DeadLetterQueue()

execution_locks: dict[str, asyncio.Lock] = {}

# -----------------------------
# Helpers
# -----------------------------


def generate_execution_id(goal: str, user_id: str) -> str:
    return hashlib.sha256(f"{user_id}:{goal}".encode()).hexdigest()


async def heartbeat_loop(execution_id: str):
    while True:
        record = store.get(execution_id)

        if not record or record.get("status") != "running":
            return

        record["heartbeat"] = time.monotonic()
        store.save(execution_id, record)

        await asyncio.sleep(2)


# -----------------------------
# Execution
# -----------------------------


async def run_agent(goal: str, user_id: str = "default"):
    if not goal.strip():
        raise HTTPException(status_code=400, detail="Goal cannot be empty")

    execution_id = generate_execution_id(goal, user_id)

    lock = execution_locks.setdefault(execution_id, asyncio.Lock())

    async with lock:
        existing = store.get(execution_id)
        if existing:
            return existing

        agent = NexusAgent(agent_id="agent_1")
        context = ExecutionContext(trace_id=agent.trace_id)

        # ✅ estado inicial correto
        store.save(
            execution_id,
            {
                "trace_id": context.trace_id,
                "execution_id": execution_id,
                "user_id": user_id,
                "status": "running",
                "started_at": context.start_wall_time,
                "heartbeat": time.monotonic(),
            },
        )

        heartbeat_task = asyncio.create_task(heartbeat_loop(execution_id))

        await user_queue_gate.acquire(user_id)
        await queue_gate.acquire(agent.trace_id)

        try:
            loop = asyncio.get_running_loop()

            result = await asyncio.wait_for(
                loop.run_in_executor(
                    process_pool,
                    agent.run,
                    AgentInput(goal=goal),
                ),
                timeout=execution_timeout,
            )

            context.finish("completed")

            response = {
                "trace_id": context.trace_id,
                "execution_id": execution_id,
                "user_id": user_id,
                "status": "completed",
                "output": result.result,
                "agent_status": result.status,
                "steps": result.steps,
                "duration": context.duration,
                "attempts": context.attempts,
            }

            store.save(execution_id, response)
            return response

        except builtins.TimeoutError:
            context.finish("failed")

            record = {
                "trace_id": context.trace_id,
                "execution_id": execution_id,
                "user_id": user_id,
                "status": "failed",
                "reason": "timeout",
                "attempts": context.attempts,
            }

            store.save(execution_id, record)
            dead_letter_queue.push(record)

            raise HTTPException(
                status_code=500,
                detail="Execution timeout",
            ) from None

        except Exception as e:
            context.finish("failed")

            record = {
                "trace_id": context.trace_id,
                "execution_id": execution_id,
                "user_id": user_id,
                "status": "failed",
                "error": str(e),
                "attempts": context.attempts,
            }

            store.save(execution_id, record)
            dead_letter_queue.push(record)

            raise HTTPException(
                status_code=500,
                detail="Execution failed",
            ) from e

        finally:
            await queue_gate.release(agent.trace_id)
            user_queue_gate.release(user_id)
            heartbeat_task.cancel()


# -----------------------------
# Replay
# -----------------------------


def replay_execution(execution_id: str):
    data = store.get(execution_id)

    if not data:
        raise HTTPException(status_code=404, detail="Execution not found")

    return data


# -----------------------------
# DLQ
# -----------------------------


async def get_dlq_items():
    if hasattr(dead_letter_queue, "all") and asyncio.iscoroutinefunction(dead_letter_queue.all):
        return await dead_letter_queue.all()

    return dead_letter_queue.all()
