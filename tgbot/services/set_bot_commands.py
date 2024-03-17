from aiogram import Bot
from aiogram.types import BotCommand
from typing import List


async def set_main_menu(bot: Bot) -> None:
    """
    Устанавливает основное меню команд для бота.

    :param bot: Экземпляр бота для установки команд.
    :type bot: Bot
    :return: None
    """
    main_menu_commands: List[BotCommand] = [
        BotCommand(command="/start", description="Запустить бота")
    ]
    await bot.set_my_commands(main_menu_commands)
