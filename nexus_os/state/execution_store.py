# ARMAZENA O ESTADO (EXECUTION CONTEXT)

import threading

from nexus_os.state.execution_context import ExecutionContext


class ExecutionStore:
    def __init__(self):
        self._store = {}
        self._lock = threading.Lock()

    def save_context(self, context: ExecutionContext):
        with self._lock:
            existing = self._store.get(context.execution_id)

            # ✅ opcional: controle de versão (proteção contra overwrite)
            if existing:
                existing_version = existing.get("version", 0)
                if context.version < existing_version:
                    raise Exception("Stale context detected")

            self._store[context.execution_id] = context.to_dict()

    def get_context(self, execution_id: str):
        with self._lock:
            data = self._store.get(execution_id)

        if not data:
            return None

        return ExecutionContext.from_dict(data)

    def exists(self, execution_id: str) -> bool:
        with self._lock:
            return execution_id in self._store

    def delete(self, execution_id: str):
        with self._lock:
            if execution_id in self._store:
                del self._store[execution_id]
