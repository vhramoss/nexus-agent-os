# CONSOME TAREFAS, PEGA DA FILA

import time

from nexus_os.core.runtime.simple_queue import task_queue
from nexus_os.core.workflow.workflow_executor import WorkflowExecutor


def start_worker():
    executor = WorkflowExecutor()

    while True:
        if task_queue.empty():
            time.sleep(1)
            continue

        task = task_queue.get()

        workflow = task["workflow"]
        execution_id = task["execution_id"]

        try:
            executor.execute(workflow, execution_id)
        except Exception as e:
            print(f"[WORKER ERROR] {e}")
