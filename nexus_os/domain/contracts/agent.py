from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentInput:
    goal: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentOutput:
    result: str | None
    steps: list[str]
    status: str
    metadata: dict[str, Any] = field(default_factory=dict)
