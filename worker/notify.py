from aiogram import Bot
from config.config import config, redis_client
from worker.fetch_data_to_sub import fetch_and_send_product_info
from worker.tasks import app, celery_event_loop
from typing import List, Optional


async def notify_task() -> None:
    """
    Отправляет подписанным пользователям обновленное сообщение с информацией о товаре.

    :return: None
    """
    subscribed_users: List[str] = await redis_client.get_subscribed_users()
    user_ids: List[int] = [int(user_id) for user_id in subscribed_users]
    bot: Bot = Bot(token=config.tg_bot.token)
    for user_id in user_ids:
        product_code: Optional[str] = await redis_client.get_user_product_code(user_id)
        if product_code:
            text: Optional[str] = await fetch_and_send_product_info(
                product_code, user_id
            )
            if text:
                await bot.send_message(chat_id=user_id, text=text, parse_mode="HTML")
    await bot.session.close()


@app.task
def stop_periodic_task() -> None:
    """
    Останавливает периодическую задачу.

    :return: None
    """
    app.control.revoke("add-every-minute", terminate=True)


@app.task
def test_task() -> None:
    """
    Запускает периодическую задачу.

    :return: None
    """
    celery_event_loop.run_until_complete(notify_task())
