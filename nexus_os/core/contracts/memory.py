from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class MemoryContext:
    recall: List[Dict[str, Any]] = field(default_factory=list)
    semantic: List[Dict[str, Any]] = field(default_factory=list)