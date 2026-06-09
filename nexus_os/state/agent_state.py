from dataclasses import dataclass, field
from typing import Any, Literal, Optional

from nexus_os.core.security.capabilities import CapabilitySet
from nexus_os.observability.event_bus import EventBus
from nexus_os.observability.tracer import Tracer


@dataclass
class AgentState:
    # já existentes
    goal: str
    status: Literal["created", "running", "completed", "failed"] = "created"
    steps: list[str] = field(default_factory=list)

    # decisão
    route: str | None = None

    # memória
    recall: list[dict[str, Any]] = field(default_factory=list)
    semantic_recall: list[dict[str, Any]] = field(default_factory=list)

    # retry global
    max_retries: int = 2

    # planner
    planner_retries: int = 0
    planner_failed: bool = False
    plan: dict[str, Any] | None = field(default_factory=dict)

    # executor
    executor_retries: int = 0
    executor_failed: bool = False
    execution_result: list[dict[str, Any]] = field(default_factory=list)

    # analyst
    analysis: str | None = None

    # tool
    tool_result: dict[str, Any] | None = None

    # reviewer
    reviewer_failed: bool = False

    # saída
    llm_output: str | None = None

    context: str | None = None
    # -----------------
    # Observability
    # -----------------
    tracer: Optional["Tracer"] = None
    event_bus: Optional["EventBus"] = None

    # Security
    capabilities: CapabilitySet | None = None
