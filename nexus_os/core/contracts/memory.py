from dataclasses import dataclass, field
from typing import Any


@dataclass
class MemoryContext:
    recall: list[dict[str, Any]] = field(default_factory=list)
    semantic: list[dict[str, Any]] = field(default_factory=list)
