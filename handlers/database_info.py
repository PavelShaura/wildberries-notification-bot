import logging
from aiogram import types, Router, F
from config.config import redis_client
from typing import List

database_info_router: Router = Router()


@database_info_router.message(F.text == "Получить информацию из БД",
                              flags={"throttling_key": "default"})
async def unsubscribe_from_updates(message: types.Message) -> None:
    """
    Обрабатывает запрос на получение информации из БД Redis и отправляет последние 5 сообщений пользователю.

    :param message: Объект сообщения от пользователя.
    :type message: aiogram.types.Message
    :return: None
    """
    user_id: int = message.from_user.id
    try:
        user_messages: List[str] = await redis_client.get_user_messages(user_id)
        user_messages.reverse()
        for msg in user_messages:
            await message.answer(msg, parse_mode="HTML")
    except Exception as e:
        await message.answer(text="В базе данных нет информации по вашей карточке.")
        logging.info(f"User_id: {user_id}. Error {e} when trying to get data from the database")
