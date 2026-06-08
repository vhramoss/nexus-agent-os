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


class Workflow:
    def __init__(self, steps: list[Step]):
        self.steps = steps
