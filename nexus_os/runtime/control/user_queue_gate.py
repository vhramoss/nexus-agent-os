import asyncio
from collections import defaultdict


class UserQueueGate:
    def __init__(self, max_per_user: int = 2):
        self.max_per_user = max_per_user
        self._locks = defaultdict(lambda: asyncio.Semaphore(max_per_user))

    async def acquire(self, user_id: str):
        await self._locks[user_id].acquire()

    def release(self, user_id: str):
        self._locks[user_id].release()
