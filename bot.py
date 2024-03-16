import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from services.set_bot_commands import set_main_menu
from services.logging_logic import register_logger, logger
from middlewares import throttling
from handlers import routers
from db.database import connect_to_db, close_db_connection


def register_global_middlewares(dp: Dispatcher, config) -> None:
    """
    Регистрирует глобальные middleware для диспетчера.

    :param dp: Диспетчер бота.
    :type dp: aiogram.Dispatcher
    :param config: Конфигурация приложения.
    :type config: config.Config
    :return: None
    """
    dp.message.middleware(throttling.ThrottlingMiddleware())


async def main() -> None:
    """
    Основная функция запуска бота.

    :return: None
    """
    from config.config import config

    register_logger()

    storage: MemoryStorage = MemoryStorage()
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher(storage=storage)

    register_global_middlewares(dp, config)

    for router in routers:
        dp.include_router(router)

    await connect_to_db()

    await set_main_menu(bot)
    try:
        await dp.start_polling(bot)
    finally:
        await close_db_connection()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Stopping bot")
