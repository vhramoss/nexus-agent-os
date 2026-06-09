# ALTERA OS ESTADOS, LÓGICA FEITA AQUI, IMPORTA A RECEITA DO PRODUTO ACTIVITY


from nexus_os.core.workflow.workflow_activity import ActivityRegistry


class WorkflowExecutor:
    def __init__(self, store, event_bus=None):
        self.store = store
        self.registry = ActivityRegistry()
        self.event_bus = event_bus

    def register_activity(self, name, func):
        self.registry.register(name, func)

    def execute(self, workflow, context):
        # ✅ marcar execução como running
        context.set_status("running")
        self.store.save_context(context)

        for step in workflow.steps:
            # ✅ verifica se step já foi executado
            existing = context.get_step(step.name)

            if existing and existing["status"] == "completed":
                continue

            # ✅ montar input baseado APENAS no contexto
            input_data = {}

            for dep in step.depends_on:
                dep_data = context.get_step(dep)

                if not dep_data or dep_data["status"] != "completed":
                    raise Exception(f"Dependency {dep} not satisfied")

                input_data[dep] = dep_data["output"]

            # ✅ evento: step started
            if self.event_bus:
                self.event_bus.publish(
                    "step.started",
                    {
                        "execution_id": context.execution_id,
                        "step": step.name,
                    },
                )

            activity = self.registry.get(step.activity)

            try:
                # ✅ execução da activity
                output = activity(input_data)

                # ✅ salvar no contexto
                context.add_step(
                    step.name,
                    {
                        "status": "completed",
                        "output": output,
                    },
                )

                # ✅ persistir estado completo
                self.store.save_context(context)

                # ✅ evento: step completed
                if self.event_bus:
                    self.event_bus.publish(
                        "step.completed",
                        {
                            "execution_id": context.execution_id,
                            "step": step.name,
                        },
                    )

            except Exception as e:
                # ✅ salvar erro no contexto
                context.add_step(
                    step.name,
                    {
                        "status": "failed",
                        "error": str(e),
                    },
                )

                context.set_error(str(e))
                self.store.save_context(context)

                # ✅ evento: step failed
                if self.event_bus:
                    self.event_bus.publish(
                        "step.failed",
                        {
                            "execution_id": context.execution_id,
                            "step": step.name,
                            "error": str(e),
                        },
                    )

                raise

        # ✅ finalizar execução
        context.set_status("completed")
        self.store.save_context(context)
