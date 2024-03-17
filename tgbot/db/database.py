from gino import Gino
from tgbot.config.config import config

DB_URL = f"postgresql://{config.db.user}:{config.db.password}@{config.db.host}:{config.db.port}/{config.db.name}"

db = Gino()


async def connect_to_db() -> None:
    """
    Устанавливает соединение с базой данных.

    :return: None
    """
    await db.set_bind(DB_URL)


async def close_db_connection() -> None:
    """
    Закрывает соединение с базой данных.

    :return: None
    """
    await db.pop_bind().close()
