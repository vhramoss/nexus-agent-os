from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class BaseEvent:
    execution_id: str
    event_type: str
    trace_id: str | None = None
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


Subscriber = Callable[[BaseEvent], None]


@dataclass
class StepStartedEvent(BaseEvent):
    step_name: str

    EVENT_TYPE = "step.started"

    def __post_init__(self):
        self.event_type = self.EVENT_TYPE


@dataclass
class StepCompletedEvent(BaseEvent):
    step_name: str
    output: dict[str, Any]

    EVENT_TYPE = "step.completed"

    def __post_init__(self):
        self.event_type = self.EVENT_TYPE


@dataclass
class ExecutionStartedEvent(BaseEvent):
    user_id: str

    EVENT_TYPE = "execution.started"

    def __post_init__(self):
        self.event_type = self.EVENT_TYPE
