from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from datetime import datetime

class AgentStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class AgentState:
    goal: str
    status: AgentStatus = AgentStatus.IDLE
    steps: List[str] = field(default_factory=list)
    route: Optional[str] = None
    started_at: datetime | None = None
    finished_at: datetime | None = None

