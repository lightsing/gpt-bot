import pickle

from redis.asyncio import Redis


class PersistentQueue:
    def __init__(
        self,
        queue_name,
        redis=None,
        namespace='persistent_queue'
    ):
        self._queue_name = queue_name
        self._redis = redis or Redis()
        self._namespace = namespace
        self._key = f"{namespace}:{queue_name}"

    async def push(self, obj):
        await self._redis.rpush(self._key, pickle.dumps(obj))

    async def pop(self):
        _, data = await self._redis.blpop(self._key)
        return pickle.loads(data)
