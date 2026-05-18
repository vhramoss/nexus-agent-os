import json
from datetime import UTC, datetime
from typing import Any

import redis.asyncio as redis


class RedisDeadLetterQueue:
    def __init__(self, redis_url: str, key: str = "nexus:dlq"):
        self.redis = redis.from_url(redis_url)
        self.key = key

    async def push(self, record: dict[str, Any]):
        record["dlq_timestamp"] = datetime.now(UTC).isoformat()

        await self.redis.rpush(self.key, json.dumps(record))

    async def all(self) -> list[dict[str, Any]]:
        items = await self.redis.lrange(self.key, 0, -1)

        return [json.loads(x.decode()) for x in items]
