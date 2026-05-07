from fastapi import FastAPI
from pydantic import BaseModel
from nexus_os.core.nexus_agent import NexusAgent

class RunRequest(BaseModel):
    goal: str

app = FastAPI(
    title = "Nexus OS API",
    description = "Agent Operating System as a Service API",
    version = "0.1.0",
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run")
def run_task(request: RunRequest):
    agent = NexusAgent(agent_id="agent_1")
    result = agent.run(goal=request.goal)
    return {
        "output": result.output,
        "status": result.metadata,
    }
