from dataclassess import dataclass
from typing import Dict, Any

@dataclass
class ToolExecution:
    name: str
    input: Dict[str, Any]
    output: Dict[str, Any]
    