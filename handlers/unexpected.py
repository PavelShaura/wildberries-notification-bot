from aiogram import Router
from aiogram.types import Message

unexpected_message_router: Router = Router()


@unexpected_message_router.message()
async def handle_unexpected_message(message: Message) -> None:
    """
    Обрабатывает все сообщения от пользователя
    не предусмотренные логикой бота.

    :param message: Объект сообщения от пользователя.
    :type message: aiogram.types.Message
    :return: None
    """
    await message.answer("Извините, я не понимаю это сообщение. Пожалуйста, используйте кнопки или команды для взаимодействия со мной.\n"
                         "/start")

