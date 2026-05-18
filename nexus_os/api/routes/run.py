from fastapi import APIRouter
from pydantic import BaseModel

from nexus_os.services.execution_service import run_agent

router = APIRouter()


class RunRequest(BaseModel):
    goal: str


@router.post("/run")
async def run_task(request: RunRequest):
    return await run_agent(request.goal)
