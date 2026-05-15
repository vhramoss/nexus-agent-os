from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from concurrent.futures import ProcessPoolExecutor
from asyncio import TimeoutError
import os
from pathlib import Path
import json

from nexus_os.core.agents.orchestrator.agent import NexusAgent

# Runtime (local)
from nexus_os.core.runtime.queue_gate import QueueGate
from nexus_os.core.runtime.dead_letter_queue import DeadLetterQueue
from nexus_os.core.runtime.supervisor import Supervisor

# Runtime (distributed – opcional)
from nexus_os.core.runtime.redis_queue_gate import RedisQueueGate
from nexus_os.core.runtime.redis_dead_letter_queue import RedisDeadLetterQueue

from nexus_os.core.contracts.agent import AgentInput
from nexus_os.core.timeline.builder import build_execution_timeline

# --------------------------------------------------
# Config
# --------------------------------------------------

MAX_CONCURRENT = int(os.getenv("NEXUS_MAX_CONCURRENT", "3"))
EXECUTION_TIMEOUT = int(os.getenv("NEXUS_EXEC_TIMEOUT", "10"))

USE_REDIS = os.getenv("NEXUS_USE_REDIS", "false").lower() == "true"
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# --------------------------------------------------
# App
# --------------------------------------------------

class RunRequest(BaseModel):
    goal: str

app = FastAPI(
    title="Nexus OS API",
    description="Agent Operating System as a Service API",
    version="0.1.0",
)

# --------------------------------------------------
# Runtime wiring
# --------------------------------------------------

process_pool = ProcessPoolExecutor(max_workers=MAX_CONCURRENT)
supervisor = Supervisor()

if USE_REDIS:
    queue_gate = RedisQueueGate(
        redis_url=REDIS_URL,
        max_concurrent=MAX_CONCURRENT,
    )
    dead_letter_queue = RedisDeadLetterQueue(redis_url=REDIS_URL)
else:
    queue_gate = QueueGate(max_concurrent=MAX_CONCURRENT)
    dead_letter_queue = DeadLetterQueue()

# --------------------------------------------------
# Health
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "ok",
        "mode": "redis" if USE_REDIS else "local",
        "max_concurrent": MAX_CONCURRENT,
    }

# --------------------------------------------------
# Run task
# --------------------------------------------------

@app.post("/run")
async def run_task(request: RunRequest):
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
                        AgentInput(goal=request.goal),
                    ),
                    timeout=EXECUTION_TIMEOUT
                )

                # ✅ DEBUG: MOSTRAR ERRO DO AGENT
                if result.status == "failed":
                    print("AGENT FAILED:")
                    print(result.result)

                return {
                    "output": result.result,
                    "agent_status": result.status,
                    "steps": result.steps,
                }

            except TimeoutError:
                print("TIMEOUT DETECTED")

                decision = supervisor.decide({
                    "reason": "timeout",
                    "attempts": attempts,
                })

            except Exception as e:
                print("MAIN EXCEPTION:", e)

                decision = supervisor.decide({
                    "reason": "exception",
                    "attempts": attempts,
                    "error": str(e),
                })

            # --------------------------------------------------
            # RETRY
            # --------------------------------------------------
            if decision == "retry":
                print("RETRY TRIGGERED")

                agent.telemetry.retry(agent.trace_id, attempts)
                attempts += 1
                continue

            # --------------------------------------------------
            # DLQ / FALLBACK
            # --------------------------------------------------
            if decision == "dlq":
                print("FALLBACK TO DLQ")

                agent.telemetry.fallback(agent.trace_id, "dlq")

                dead_letter_queue.push({
                    "trace_id": agent.trace_id,
                    "goal": request.goal,
                    "reason": decision,
                })

                raise HTTPException(
                    status_code=500,
                    detail="Execution sent to dead-letter queue"
                )

            raise HTTPException(
                status_code=500,
                detail="Execution aborted by supervisor"
            )

    finally:
        queue_gate.release(agent.trace_id)

# --------------------------------------------------
# DLQ inspection
# --------------------------------------------------

@app.get("/dlq")
def get_dlq():
    return {
        "items": dead_letter_queue.all()
    }

# --------------------------------------------------
# Replay
# --------------------------------------------------

@app.get("/replay/{trace_id}")
def replay(trace_id: str):
    path = Path("events") / f"{trace_id}.jsonl"

    if not path.exists():
        return {"error": "trace not found"}

    # ✅ carregar eventos
    events = []
    with path.open() as f:
        for line in f:
            events.append(json.loads(line))

    # ✅ construir timeline
    timeline = build_execution_timeline(events)

    # ✅ extrair input/output
    input_data = None
    result_data = None

    for event in events:
        if event["event_type"] == "agent.started":
            input_data = event.get("metadata", {})

        if event["event_type"] == "agent.completed":
            result_data = event.get("metadata", {})

    return {
        "trace_id": trace_id,
        "input": input_data,
        "timeline": timeline,
        "result": result_data,
    }