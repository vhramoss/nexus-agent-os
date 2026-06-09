# COLOCA TAREFAS NA FILA (PRODUCER)

from nexus_os.core.runtime.simple_queue import task_queue


def dispatch_task(task_data: dict):
    task_queue.put(task_data)
