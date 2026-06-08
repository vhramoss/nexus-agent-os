from nexus_os.core.runtime.execution_store import ExecutionStore
from nexus_os.core.workflow.activity import ActivityRegistry


class WorkflowExecutor:
    def __init__(self, event_bus=None):
        self.store = ExecutionStore()
        self.registry = ActivityRegistry()
        self.event_bus = event_bus

    def register_activity(self, name, func):
        self.registry.register(name, func)

    def execute(self, workflow, execution_id: str):
        results: dict[str, any] = {}

        saved_steps = self.store.get_steps(execution_id)

        for step in workflow.steps:
            # ✅ já executado
            if step.name in saved_steps:
                results[step.name] = saved_steps[step.name]["output"]
                continue

            # ✅ dependencies
            for dep in step.depends_on:
                if dep not in results:
                    raise Exception(f"Dependency {dep} not satisfied")

            # ✅ evento start
            if self.event_bus:
                self.event_bus.publish(
                    "step.started",
                    {
                        "execution_id": execution_id,
                        "step": step.name,
                    },
                )

            activity = self.registry.get(step.activity)

            try:
                output = activity(results)

                # ✅ persistência
                self.store.save_step(
                    execution_id,
                    step.name,
                    {
                        "status": "completed",
                        "output": output,
                    },
                )

                results[step.name] = output

                # ✅ evento success
                if self.event_bus:
                    self.event_bus.publish(
                        "step.completed",
                        {
                            "execution_id": execution_id,
                            "step": step.name,
                            "output": str(output),
                        },
                    )

            except Exception as e:
                # ✅ persistência erro
                self.store.save_step(
                    execution_id,
                    step.name,
                    {
                        "status": "failed",
                        "error": str(e),
                    },
                )

                # ✅ evento erro
                if self.event_bus:
                    self.event_bus.publish(
                        "step.failed",
                        {
                            "execution_id": execution_id,
                            "step": step.name,
                            "error": str(e),
                        },
                    )

                raise

        return results
