from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Literal
from nexus_os.core.security.capabilities import CapabilitySet

from typing import TYPE_CHECKING


from nexus_os.core.observability.tracer import Tracer
from nexus_os.core.observability.event_bus import EventBus



@dataclass
class AgentState:
    # já existentes
    goal: str
    status: Literal["created", "running", "completed", "failed"] = "created"
    steps: List[str] = field(default_factory=list)

    # decisão
    route: Optional[str] = None

    # memória
    recall: List[Dict[str, Any]] = field(default_factory=list)
    semantic_recall: List[Dict[str, Any]] = field(default_factory=list)

    # retry global
    max_retries: int = 2

    # planner
    planner_retries: int = 0
    planner_failed: bool = False
    plan: Optional[Dict[str, Any]] = None

    # executor
    executor_retries: int = 0
    executor_failed: bool = False
    execution_result: List[Dict[str, Any]] = field(default_factory=list)

    # analyst
    analysis: Optional[str] = None

    # tool
    tool_result: Optional[Dict[str, Any]] = None

    # reviewer
    reviewer_failed: bool = False

    # saída
    llm_output: Optional[str] = None

    context: Optional[str] = None
    # -----------------
    # Observability 
    # -----------------
    tracer: Optional["Tracer"] = None
    event_bus: Optional["EventBus"] = None

    #Security
    capabilities: Optional[CapabilitySet] = None

