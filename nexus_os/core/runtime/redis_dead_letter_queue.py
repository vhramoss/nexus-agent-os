import redis
import json
from typing import Dict, Any
from datetime import datetime, timezone


class RedisDeadLetterQueue:
    def __init__(self, redis_url: str, key: str = "nexus:dlq"):
        self.redis = redis.Redis.from_url(redis_url)
        self.key = key

    def push(self, record: Dict[str, Any]):
        record["dlq_timestamp"] = datetime.now(timezone.utc).isoformat()
        self.redis.rpush(self.key, json.dumps(record))

    def all(self):
        return [json.loads(x) for x in self.redis.lrange(self.key, 0, -1)]