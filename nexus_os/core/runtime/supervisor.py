from typing import Dict, Any


class Supervisor:
    """
    Supervisor simples baseado em regras.
    Em produção, isso pode evoluir para árvores ou LLMs.
    """

    def decide(self, context: Dict[str, Any]) -> str:
        """
        Retorna uma decisão:
        - 'retry'
        - 'dlq'
        - 'abort'
        """

        reason = context.get("reason")
        attempts = context.get("attempts", 0)

        # ⏱️ Timeout é falha definitiva
        if reason == "timeout":
            return "dlq"

        # 💥 Exceção inesperada
        if reason == "exception":
            if attempts < 1:
                return "retry"
            return "dlq"

        # ✅ Default seguro
        return "abort"