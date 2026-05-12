from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AgentState:
    # já existentes
    goal: str
    status: Any = None
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
    execution_result: List[str] = field(default_factory=list)

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
    tracer: Optional[Any] = None
    event_bus: Optional[Any] = None

