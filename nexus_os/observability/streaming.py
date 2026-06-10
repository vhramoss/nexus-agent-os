from fastapi import WebSocket

from nexus_os.observability.event_types import BaseEvent
from nexus_os.observability.timeline_builder import TimelineBuilder


class EventStreamer:
    def __init__(self):
        # execution_id → [clients]
        self.clients: dict[str, list[WebSocket]] = {}

        # execution_id → eventos acumulados
        self.buffers: dict[str, list[dict]] = {}

        self.builder = TimelineBuilder()

    def register(self, execution_id: str, client: WebSocket):
        self.clients.setdefault(execution_id, []).append(client)

    def unregister(self, execution_id: str, client: WebSocket):
        if execution_id in self.clients:
            self.clients[execution_id].remove(client)

            if not self.clients[execution_id]:
                del self.clients[execution_id]

    def handle(self, event: BaseEvent):
        execution_id = event.execution_id

        # ✅ guarda evento no buffer
        self.buffers.setdefault(execution_id, []).append(event.to_dict())

        # ✅ constrói estado atualizado
        state = self.builder.build(self.buffers[execution_id])

        if execution_id not in self.clients:
            return

        for client in list(self.clients[execution_id]):
            try:
                client.send_json(state)
            except Exception:
                self.unregister(execution_id, client)
