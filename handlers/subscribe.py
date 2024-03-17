import logging
from aiogram import types, Router, F
from db.pg_manager import query_manager
from config.config import redis_client
from worker.notify import test_task
from typing import Optional

subscribe_router: Router = Router()


@subscribe_router.callback_query(F.data == "sub", flags={"throttling_key": "callback"})
async def subscribe_to_updates(call: types.CallbackQuery) -> None:
    """
    Подписывает пользователя на обновленное сообщение
     с информацией о товаре с интервалом 5 минут.

    :param call: Объект callback-запроса.
    :type call: aiogram.types.CallbackQuery
    :return: None
    """
    username: Optional[str] = call.from_user.username
    user_id: int = call.from_user.id
    product_code: Optional[str] = await query_manager.get_latest_query_by_user_id(
        user_id
    )
    if product_code:
        await redis_client.add_subscribed_user(user_id)
        await redis_client.set_user_product_code(user_id, product_code)
        await call.message.answer(f"Вы подписались на уведомления по товару: \n")
        test_task.delay()
        logging.info(
            f"User: {username}, ID: {user_id} successfully subscribed to notifications!"
        )
    else:
        logging.info(
            f"Subscription denied for user: {username}, ID: {user_id}, no product code in db!"
        )
