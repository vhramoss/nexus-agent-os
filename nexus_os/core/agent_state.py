from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any
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
    llm_output: Optional[str] = None
    retries: int = 0
    max_retries: int = 2
    llm_failed:bool = False
    recall: List[Dict[str, Any]] = field(default_factory=list)
    semantic_recall: list = field(default_factory=list)
    
