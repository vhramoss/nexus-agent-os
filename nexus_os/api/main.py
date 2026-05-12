from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from concurrent.futures import ProcessPoolExecutor

from nexus_os.core.nexus_agent import NexusAgent
from nexus_os.core.runtime.queue_gate import QueueGate


class RunRequest(BaseModel):
    goal: str


app = FastAPI(
    title="Nexus OS API",
    description="Agent Operating System as a Service API",
    version="0.1.0",
)

# 🔒 Limite global de concorrência
queue_gate = QueueGate(max_concurrent=3)

# ✅ Pool de processos (CPU-bound REAL)
process_pool = ProcessPoolExecutor(max_workers=3)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/run")
async def run_task(request: RunRequest):
    agent = NexusAgent(agent_id="agent_1")

    # ⏳ Fila
    await queue_gate.acquire(agent.trace_id)

    try:
        loop = asyncio.get_running_loop()

        # ✅ Execução pesada fora do event loop
        result = await loop.run_in_executor(
            process_pool,
            agent.run,
            request.goal
        )

        return {
            "output": result.output,
            "status": result.metadata,
        }
    finally:
        # ✅ Sempre libera vaga
        queue_gate.release(agent.trace_id)
