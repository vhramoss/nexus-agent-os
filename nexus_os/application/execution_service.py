# ORQUESTRADOR DA EXECUÇÃO

import asyncio
import hashlib

from fastapi import HTTPException

from nexus_os.core.runtime.dispatcher import dispatch_task
from nexus_os.core.workflow.workflow_executor import WorkflowExecutor
from nexus_os.core.workflow.workflow_models import Step, Workflow
from nexus_os.domain.agents.orchestrator.agent import NexusAgent
from nexus_os.infra.config import get_settings
from nexus_os.observability.event_bus import EventBus
from nexus_os.runtime.control.queue_gate import QueueGate
from nexus_os.runtime.control.supervisor import Supervisor
from nexus_os.runtime.control.user_queue_gate import UserQueueGate
from nexus_os.runtime.redis.redis_queue_gate import RedisQueueGate
from nexus_os.runtime.resilience.dead_letter_queue import DeadLetterQueue
from nexus_os.runtime.resilience.redis_dead_letter_queue import RedisDeadLetterQueue
from nexus_os.state.execution_context import ExecutionContext
from nexus_os.state.execution_store import ExecutionStore

# -----------------------------
# Config
# -----------------------------

settings = get_settings()

max_concurrent = settings.max_concurrent
use_redis = settings.use_redis
redis_url = settings.redis_url

# -----------------------------
# Runtime
# -----------------------------

supervisor = Supervisor()
user_queue_gate = UserQueueGate(max_per_user=2)
store = ExecutionStore()

event_bus = EventBus()
workflow_executor = WorkflowExecutor(store=store, event_bus=event_bus)

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


# -----------------------------
# Execution (CONTEXT-FIRST)
# -----------------------------


async def run_agent(goal: str, user_id: str = "default"):
    if not goal.strip():
        raise HTTPException(status_code=400, detail="Goal cannot be empty")

    execution_id = generate_execution_id(goal, user_id)
    lock = execution_locks.setdefault(execution_id, asyncio.Lock())

    async with lock:
        existing = store.get_context(execution_id)

        if existing:
            return existing.to_dict()

        agent = NexusAgent(agent_id="agent_1")

        # ✅ criar contexto (SOURCE OF TRUTH)
        context = ExecutionContext(
            execution_id=execution_id,
            user_id=user_id,
            trace_id=agent.trace_id,
        )

        context.set_status("queued")

        # ✅ persistir contexto
        store.save_context(context)

        # ✅ evento
        event_bus.publish(
            "execution.started",
            {
                "execution_id": execution_id,
                "user_id": user_id,
            },
        )

        # ✅ registrar activity (context-first input)
        workflow_executor.register_activity(
            "agent_run",
            lambda inputs: agent.run(inputs),  # agora recebe dict de deps
        )

        # ✅ definir workflow
        workflow = Workflow(
            steps=[
                Step("agent_run", "agent_run"),
            ]
        )

        # ✅ enviar para fila
        dispatch_task(
            {
                "execution_id": execution_id,
                "workflow": workflow,
            }
        )

        return {
            "execution_id": execution_id,
            "status": "queued",
        }


# -----------------------------
# Replay (AGORA PRINCIPAL)
# -----------------------------


def replay_execution(execution_id: str):
    context = store.get_context(execution_id)

    if not context:
        raise HTTPException(status_code=404, detail="Execution not found")

    return context.to_dict()


# -----------------------------
# DLQ
# -----------------------------


async def get_dlq_items():
    if hasattr(dead_letter_queue, "all") and asyncio.iscoroutinefunction(dead_letter_queue.all):
        return await dead_letter_queue.all()

    return dead_letter_queue.all()
