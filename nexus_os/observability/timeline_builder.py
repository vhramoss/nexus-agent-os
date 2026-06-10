from typing import Any


class TimelineBuilder:
    def build(self, events: list[dict]) -> dict[str, Any]:
        timeline = {
            "execution_id": None,
            "status": "unknown",
            "steps": {},
        }

        for event in events:
            event_type = event.get("event_type")
            execution_id = event.get("execution_id")

            if execution_id:
                timeline["execution_id"] = execution_id

            if event_type == "execution.started":
                timeline["status"] = "running"

            elif event_type == "execution.finished":
                timeline["status"] = "completed"

            elif event_type == "execution.failed":
                timeline["status"] = "failed"

            elif event_type == "step.started":
                step = event.get("step_name")

                timeline["steps"][step] = {
                    "status": "running",
                    "output": None,
                }

            elif event_type == "step.completed":
                step = event.get("step_name")

                timeline["steps"][step] = {
                    "status": "completed",
                    "output": event.get("output"),
                }

            elif event_type == "step.failed":
                step = event.get("step_name")

                timeline["steps"][step] = {
                    "status": "failed",
                    "error": event.get("error"),
                }

        return timeline
