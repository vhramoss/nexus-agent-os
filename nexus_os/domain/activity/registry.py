# COMO EXECUTAR A RECEITA DO PRODUTO

from collections.abc import Callable


class ActivityRegistry:
    def __init__(self):
        self.activities: dict[str, Callable] = {}

    def register(self, name: str, func: Callable):
        self.activities[name] = func

    def get(self, name: str):
        if name not in self.activities:
            raise Exception(f"Activity {name} not registered")

        return self.activities[name]
