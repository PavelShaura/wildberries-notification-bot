import aioredis
from pydantic import BaseModel
from pydantic.v1 import BaseSettings

from redis_client.client import AsyncRedisClient


class DbConfig(BaseModel):
    name: str
    user: str
    password: str
    host: str
    port: int


class TgBot(BaseModel):
    token: str


class DbRedis(BaseModel):
    host: str
    port: int


class Config(BaseModel):
    tg_bot: TgBot
    db: DbConfig = None
    redis: DbRedis =None


def load_config(path: str = ".env") -> Config:
    """
    Загружает конфигурацию из переменных окружения.

    Args:
        path (str): Путь к файлу окружения. По умолчанию ".env".

    return:
        Config: Загруженная конфигурация.
    """
    from pathlib import Path

    class Settings(BaseSettings):
        BOT_TOKEN: str
        DB_NAME: str
        DB_USER: str
        DB_PASSWORD: str
        DB_HOST: str
        DB_PORT: int
        REDIS_HOST: str
        REDIS_PORT: int

        class Config:
            env_file = Path(path)
            env_file_encoding = 'utf-8'

    settings = Settings()
    return Config(
        tg_bot=TgBot(
            token=settings.BOT_TOKEN
        ),
        db=DbConfig(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            name=settings.DB_NAME,
            password=settings.DB_PASSWORD,
            user=settings.DB_USER
        ),
        redis=DbRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT
        )
    )


config = load_config(".env")

redis_instance = aioredis.Redis(
        host=config.redis.host,
        port=config.redis.port,
        decode_responses=True
    )

redis_client = AsyncRedisClient(redis_instance)