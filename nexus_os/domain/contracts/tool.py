from dataclasses import dataclass
from typing import Any


@dataclass
class ToolExecution:
    name: str
    input: dict[str, Any]
    output: dict[str, Any]
