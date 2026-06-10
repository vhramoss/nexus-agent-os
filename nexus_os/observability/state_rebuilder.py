from typing import Any


class StateRebuilder:
    def __init__(self, state_machine):
        self.state_machine = state_machine

    def rebuild(self, events: list[dict[str, Any]]) -> dict[str, Any]:
        state = {
            "status": "created",
            "steps": {},
            "current_step": None,
        }

        for event in events:
            state = self.state_machine.apply(state, event)

        return state
