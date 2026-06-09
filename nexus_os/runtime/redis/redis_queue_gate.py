import asyncio

import redis.asyncio as redis
from nexus_os.observability.event_bus import EventBus

# -----------------------------
# LUA SCRIPT (ATÔMICO)
# -----------------------------
ACQUIRE_LUA = """
local current = tonumber(redis.call('GET', KEYS[1]) or '0')
local max = tonumber(ARGV[1])

if current < max then
    redis.call('INCR', KEYS[1])
    return 1
else
    return 0
end
"""


class RedisQueueGate:
    def __init__(
        self,
        redis_url: str,
        key: str = "nexus:queue",
        max_concurrent: int = 3,
        event_bus: EventBus | None = None,
    ):
        self.redis = redis.from_url(redis_url)
        self.key = key
        self.max_concurrent = max_concurrent
        self.event_bus = event_bus

        self._acquire_script = None

    async def _load_script(self):
        if self._acquire_script is None:
            self._acquire_script = self.redis.register_script(ACQUIRE_LUA)

    async def acquire(self, trace_id: str):
        await self._load_script()

        while True:
            acquired = await self._acquire_script(
                keys=[self.key],
                args=[self.max_concurrent],
            )

            if acquired == 1:
                break

            await asyncio.sleep(0.05)

        if self.event_bus:
            self.event_bus.publish(
                "agent.dequeued",
                {"trace_id": trace_id},
            )

    async def release(self, trace_id: str):
        current = await self.redis.decr(self.key)

        # proteção contra underflow
        if current < 0:
            await self.redis.set(self.key, 0)

        if self.event_bus:
            self.event_bus.publish(
                "agent.released",
                {"trace_id": trace_id},
            )
