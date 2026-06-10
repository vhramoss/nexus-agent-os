from typing import Any


class StateMachine:
    def apply(self, state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
        event_type = event.get("event_type")

        # ==========================================================
        # EXECUTION
        # ==========================================================

        if event_type == "execution.started":
            state["status"] = "running"

        elif event_type == "execution.finished":
            state["status"] = "completed"

        elif event_type == "execution.failed":
            state["status"] = "failed"

        # ==========================================================
        # STEPS
        # ==========================================================

        elif event_type == "step.started":
            step = event.get("step_name")

            state["steps"][step] = {
                "status": "running",
                "output": None,
                "error": None,
            }

            state["current_step"] = step

        elif event_type == "step.completed":
            step = event.get("step_name")

            state["steps"][step] = {
                "status": "completed",
                "output": event.get("output"),
                "error": None,
            }

            state["current_step"] = None

        elif event_type == "step.failed":
            step = event.get("step_name")

            state["steps"][step] = {
                "status": "failed",
                "output": None,
                "error": event.get("error"),
            }

            state["current_step"] = None

        return state
