import logging
import re
from typing import Optional

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tgbot.db.pg_manager import query_manager
from tgbot.keyboards.inline import subscribe
from tgbot.worker.fetch_data_to_sub import fetch_and_send_product_info

get_product_router: Router = Router()


@get_product_router.message(
    F.text == "Получить информацию по товару", flags={"throttling_key": "default"}
)
async def get_code_info(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает запрос на получение информации по товару и переводит пользователя в состояние ожидания ввода кода.

    :param message: Сообщение от пользователя.
    :type message: aiogram.types.Message
    :param state: Контекст состояния FSM.
    :type state: aiogram.fsm.context.FSMContext
    :return: None
    """
    await message.answer(text="Напишите в чат код товара ⤵️")
    await state.set_state("input_code")


@get_product_router.message(
    StateFilter("input_code"), flags={"throttling_key": "default"}
)
async def give_the_product(message: Message, state: FSMContext) -> None:
    """
    Получает код товара от пользователя, обрабатывает его и
    при успешном получении строки от fetch_and_send_product_info()
    отправляет сообщение с информацией о товаре пользователю.

    :param message: Сообщение от пользователя.
    :type message: aiogram.types.Message
    :param state: Контекст состояния FSM.
    :type state: aiogram.fsm.context.FSMContext
    :return: None
    """
    user_id: int = message.from_user.id
    product_code: str = message.text.strip()
    pattern: str = r"^\d{7,10}$"  # Проверка, что код товара состоит из 7 до 10 цифр
    if not re.match(pattern, product_code):
        await message.answer(
            "Неверный формат кода продукта. Код должен состоять от 7 до 10 цифр.\n\n"
            "Напишите в чат кода товара ⤵️"
        )
        return
    await query_manager.save_query(user_id, product_code)
    try:
        text: Optional[str] = await fetch_and_send_product_info(product_code, user_id)
        if text:
            await message.answer(text=text, reply_markup=subscribe, parse_mode="HTML")
            await state.clear()
        else:
            await message.answer(
                text=f"Информация по коду <code>{product_code}</code> не найдена.\n\n"
                f"Напишите в чат кода товара ⤵️",
                parse_mode="HTML",
            )
    except Exception as e:
        await message.answer(
            text=f"Произошла ошибка при получении информации по коду <code>{product_code}</code>.\n\n"
            f"Напишите в чат кода товара ⤵️",
            parse_mode="HTML",
        )
        logging.info(f"There was an error {e} while processing the code {product_code}")
