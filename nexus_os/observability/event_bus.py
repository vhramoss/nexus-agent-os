from nexus_os.observability.event_types import BaseEvent, Subscriber


class EventBus:
    def __init__(self):
        self.subscribers: dict[str, list[Subscriber]] = {}

    def subscribe(self, event_type: str, callback: Subscriber) -> None:
        self.subscribers.setdefault(event_type, []).append(callback)

    def publish(self, event: BaseEvent) -> None:
        event_type = event.event_type

        # Subscribers específicos
        for callback in self.subscribers.get(event_type, []):
            try:
                callback(event)
            except Exception as e:
                print(f"[EventBus] subscriber error: {e}")

        # Subscribers globais
        for callback in self.subscribers.get("*", []):
            try:
                callback(event)
            except Exception as e:
                print(f"[EventBus] subscriber error: {e}")
