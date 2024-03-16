from aioredis import Redis
from typing import List, Optional


class AsyncRedisClient(Redis):
    """
    Асинхронный клиент для работы с Redis.
    """

    def __init__(self, redis_instance: Redis, *args, **kwargs):
        """
        Инициализация асинхронного клиента Redis.

        :param redis_instance: Экземпляр клиента Redis.
        :type redis_instance: aioredis.Redis
        """
        super().__init__(*args, **kwargs)
        self.redis = redis_instance

    async def get_user_messages(self, user_id: int, limit: int = 5) -> List[str]:
        """Получить последние сообщения пользователя."""
        return await self.redis.lrange(f"user_messages:{user_id}", 0, limit - 1)

    async def add_subscribed_user(self, user_id: int) -> None:
        """Добавить пользователя в подписчики."""
        await self.redis.sadd('subscribed_users', str(user_id))

    async def set_user_product_code(self, user_id: int, product_code: str) -> None:
        """Сохранить код продукта пользователя."""
        await self.redis.set(f'user_id:{user_id}', product_code)

    async def remove_subscribed_user(self, user_id: int) -> None:
        """Удалить пользователя из подписчиков."""
        await self.redis.srem('subscribed_users', str(user_id))

    async def add_user_message(self, user_id: int, message: str) -> None:
        """Добавить сообщение пользователя и ограничить длину списка до 5 элементов."""
        await self.redis.lpush(f"user_messages:{user_id}", message)
        await self.redis.ltrim(f"user_messages:{user_id}", 0, 4)

    async def get_subscribed_users(self) -> List[str]:
        """Получить список подписчиков."""
        return await self.redis.smembers('subscribed_users')

    async def get_user_product_code(self, user_id: int) -> Optional[str]:
        """Получить код продукта пользователя."""
        return await self.redis.get(f'user_id:{user_id}')
