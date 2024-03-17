import logging
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.reply import menu_keyboard

command_start_router: Router = Router()


@command_start_router.message(CommandStart(), flags={"throttling_key": "default"})
async def user_start(message: Message) -> None:
    """
    Обрабатывает команду старта от пользователя и отправляет приветственное сообщение с меню.

    :param message: Сообщение от пользователя.
    :type message: aiogram.types.Message
    :return: None
    """
    user_id: int = message.from_user.id
    name: str = message.from_user.full_name
    photo_url: str = (
        "https://selsup.ru/wp-content/webp-express/webp-images/uploads/2022/12/20221206_160148_0000.png.webp"
    )
    await message.answer_photo(
        photo=photo_url,
        caption=f"Приветствуем тебя, <b>{name}</b>!\n\n"
        f"Этот бот умеет получать информацию о товаре с маркетплейса <b>WILDBERRIES</b> "
        f"по артикулу товара.\n\n"
        f"📌 Название, 🔢 артикул, 📈 цена, 🏅 рейтинг товара, 🔍  количество товара на всех складах\n\n"
        f"<i>А также Вы можете подписаться на уведомления по вашей карточке.</i>",
        reply_markup=menu_keyboard,
        parse_mode="HTML",
    )
    logging.info(f"User:{name}, ID:{user_id} came to see us!")
