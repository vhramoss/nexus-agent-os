from enum import Enum
from typing import TypedDict


class Decision(str, Enum):
    RETRY = "retry"
    DLQ = "dlq"
    ABORT = "abort"


class SupervisorContext(TypedDict, total=False):
    reason: str
    attempts: int
    error: str


class Supervisor:
    """
    Supervisor baseado em regras determinísticas.
    """

    def decide(self, context: SupervisorContext) -> Decision:
        reason = context.get("reason")
        attempts = context.get("attempts", 0)

        # ⏱️ Timeout é falha definitiva
        if reason == "timeout":
            return Decision.DLQ

        # 💥 Exceção inesperada
        if reason == "exception":
            if attempts < 1:
                return Decision.RETRY
            return Decision.DLQ

        # ✅ fallback seguro
        return Decision.ABORT
