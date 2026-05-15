from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

@dataclass
class AgentInput:
    goal: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AgentOutput:
    result: Optional[str]
    steps: List[str]
    status: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    