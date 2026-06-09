# O QUE DEVE SER FEITO COM O PRODUTO


class Step:
    def __init__(
        self,
        name: str,
        activity: str,
        depends_on: list[str] | None = None,
    ):
        self.name = name
        self.activity = activity
        self.depends_on = depends_on or []

    def __repr__(self):
        return f"Step(name={self.name}, activity={self.activity})"


class Workflow:
    def __init__(self, steps: list[Step]):
        if not steps:
            raise ValueError("Workflow must have at least one step")

        names = [s.name for s in steps]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate step names detected")

        self.steps = list(steps)

    def __repr__(self):
        return f"Workflow(steps={self.steps})"
