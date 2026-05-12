import asyncio
import redis.asyncio as redis
from typing import Optional
from nexus_os.core.observability.event_bus import EventBus


class RedisQueueGate:
    """
    QueueGate distribuído via Redis.
    """

    def __init__(
        self,
        redis_url: str,
        key: str = "nexus:queue",
        max_concurrent: int = 3,
        event_bus: Optional[EventBus] = None,
    ):
        self.redis = redis.from_url(redis_url)
        self.key = key
        self.max_concurrent = max_concurrent
        self.event_bus = event_bus

    async def acquire(self, trace_id: str):
        while True:
            current = await self.redis.get(self.key)
            current = int(current or 0)

            if current < self.max_concurrent:
                await self.redis.incr(self.key)
                break

            await asyncio.sleep(0.1)

        if self.event_bus:
            self.event_bus.publish(
                "agent.dequeued",
                {"trace_id": trace_id, "current": current + 1},
            )

    async def release(self, trace_id: str):
        await self.redis.decr(self.key)

        if self.event_bus:
            self.event_bus.publish(
                "agent.released",
                {"trace_id": trace_id},
            )