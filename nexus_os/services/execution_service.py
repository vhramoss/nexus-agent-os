import asyncio
import builtins
from concurrent.futures import ProcessPoolExecutor

from fastapi import HTTPException

from nexus_os.core.agents.orchestrator.agent import NexusAgent
from nexus_os.core.contracts.agent import AgentInput
from nexus_os.core.runtime.dead_letter_queue import DeadLetterQueue
from nexus_os.core.runtime.queue_gate import QueueGate
from nexus_os.core.runtime.redis_dead_letter_queue import RedisDeadLetterQueue
from nexus_os.core.runtime.redis_queue_gate import RedisQueueGate
from nexus_os.core.runtime.supervisor import Supervisor
from nexus_os.infra.config import get_settings

# --------------------------------------------------
# Config
# --------------------------------------------------

settings = get_settings()

max_concurrent = settings.max_concurrent
execution_timeout = settings.exec_timeout
use_redis = settings.use_redis
redis_url = settings.redis_url

# --------------------------------------------------
# Runtime wiring
# --------------------------------------------------

process_pool = ProcessPoolExecutor(max_workers=max_concurrent)
supervisor = Supervisor()

if use_redis:
    queue_gate = RedisQueueGate(redis_url=redis_url, max_concurrent=max_concurrent)
    dead_letter_queue = RedisDeadLetterQueue(redis_url=redis_url)
else:
    queue_gate = QueueGate(max_concurrent=max_concurrent)
    dead_letter_queue = DeadLetterQueue()

# --------------------------------------------------
# Execution
# --------------------------------------------------


async def run_agent(goal: str):
    if not goal.strip():
        raise HTTPException(status_code=400, detail="Goal cannot be empty")

    agent = NexusAgent(agent_id="agent_1")
    attempts = 0

    await queue_gate.acquire(agent.trace_id)

    try:
        loop = asyncio.get_running_loop()

        while True:
            try:
                result = await asyncio.wait_for(
                    loop.run_in_executor(
                        process_pool,
                        agent.run,
                        AgentInput(goal=goal),
                    ),
                    timeout=execution_timeout,
                )

                return {
                    "trace_id": agent.trace_id,
                    "output": result.result,
                    "agent_status": result.status,
                    "steps": result.steps,
                }

            except builtins.TimeoutError:
                decision = supervisor.decide(
                    {
                        "reason": "timeout",
                        "attempts": attempts,
                    }
                )

            except Exception as e:
                decision = supervisor.decide(
                    {
                        "reason": "exception",
                        "attempts": attempts,
                        "error": str(e),
                    }
                )

            if decision == "retry":
                attempts += 1
                continue

            if decision == "dlq":
                dead_letter_queue.push(
                    {
                        "trace_id": agent.trace_id,
                        "goal": goal,
                        "reason": decision,
                    }
                )

                raise HTTPException(
                    status_code=500,
                    detail="Execution sent to dead-letter queue",
                )

            raise HTTPException(
                status_code=500,
                detail="Execution aborted by supervisor",
            )

    finally:
        queue_gate.release(agent.trace_id)


def get_dlq_items():
    return dead_letter_queue.all()
