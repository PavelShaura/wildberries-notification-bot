import logging
from aiogram import types, Router, F
from config.config import redis_client
from worker.notify import stop_periodic_task
from typing import Optional

unsubscribe_router: Router = Router()


@unsubscribe_router.message(F.text == "Остановить уведомления", flags={"throttling_key": "default"})
async def unsubscribe_from_updates(message: types.Message) -> None:
    """
    Останавливает уведомления для пользователя и удаляет его из списка подписчиков в БД Redis.

    :param message: Объект сообщения от пользователя.
    :type message: aiogram.types.Message
    :return: None
    """
    name: Optional[str] = message.from_user.full_name
    user_id: int = message.from_user.id
    stop_periodic_task.delay()
    await redis_client.remove_subscribed_user(user_id)
    await message.answer("Вы отписались от уведомлений.")
    logging.info(f"User: {name}, ID: {user_id} unsubscribed from notifications! ")
