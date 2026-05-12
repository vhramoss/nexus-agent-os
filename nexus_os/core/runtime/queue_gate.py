import asyncio
from typing import Optional
from nexus_os.core.observability.event_bus import EventBus


class QueueGate:
    def __init__(self, max_concurrent: int, event_bus: Optional[EventBus] = None):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.max_concurrent = max_concurrent
        self.event_bus = event_bus

    async def acquire(self, trace_id: str):
        if self.event_bus:
            self.event_bus.publish(
                "agent.queued",
                {
                    "trace_id": trace_id,
                    "max_concurrent": self.max_concurrent,
                },
            )

        await self.semaphore.acquire()

        if self.event_bus:
            self.event_bus.publish(
                "agent.dequeued",
                {
                    "trace_id": trace_id,
                    "current_slots": self.semaphore._value,
                },
            )

    def release(self, trace_id: str):
        self.semaphore.release()

        if self.event_bus:
            self.event_bus.publish(
                "agent.released",
                {
                    "trace_id": trace_id,
                    "current_slots": self.semaphore._value,
                },
            )