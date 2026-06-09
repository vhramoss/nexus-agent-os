# ESTADO ATUAL + RELATÓRIO DO QUE JÀ ACONTECEU + DECISÕES TOMADAS

import time


class Status:
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ExecutionContext:
    def __init__(self, execution_id: str, user_id: str, trace_id: str):
        self.execution_id = execution_id
        self.user_id = user_id
        self.trace_id = trace_id

        self.status = Status.CREATED
        self.started_at = time.time()
        self.updated_at = self.started_at
        self.version = 0

        self.steps = {}
        self.metadata = {}
        self.error = None
        self.attempts = 0

    def _touch(self):
        self.updated_at = time.time()
        self.version += 1

    def set_status(self, status: str):
        self.status = status
        self._touch()

    def finish(self):
        self.set_status(Status.COMPLETED)

    def set_error(self, error: str):
        self.error = error
        self.set_status(Status.FAILED)

    def start_step(self, step_name: str):
        self.steps[step_name] = {
            "status": Status.RUNNING,
            "started_at": time.time(),
        }
        self._touch()

    def complete_step(self, step_name: str, output):
        self.steps[step_name] = {
            "status": Status.COMPLETED,
            "output": output,
            "finished_at": time.time(),
        }
        self._touch()

    def fail_step(self, step_name: str, error: str):
        self.steps[step_name] = {
            "status": Status.FAILED,
            "error": error,
            "finished_at": time.time(),
        }
        self._touch()

    def get_step(self, step_name: str):
        return self.steps.get(step_name)

    def to_dict(self):
        return {
            "execution_id": self.execution_id,
            "user_id": self.user_id,
            "trace_id": self.trace_id,
            "status": self.status,
            "started_at": self.started_at,
            "updated_at": self.updated_at,
            "version": self.version,
            "steps": self.steps,
            "metadata": self.metadata,
            "error": self.error,
            "attempts": self.attempts,
        }

    @classmethod
    def from_dict(cls, data: dict):
        obj = cls(
            execution_id=data["execution_id"],
            user_id=data["user_id"],
            trace_id=data["trace_id"],
        )

        obj.status = data.get("status")
        obj.started_at = data.get("started_at")
        obj.updated_at = data.get("updated_at")
        obj.version = data.get("version", 0)
        obj.steps = data.get("steps", {})
        obj.metadata = data.get("metadata", {})
        obj.error = data.get("error")
        obj.attempts = data.get("attempts", 0)

        return obj
