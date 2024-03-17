from datetime import datetime
from sqlalchemy import select
from db.models import Query
from db.database import db as db_instance
from typing import Optional


class QueryManager:
    """
    Менеджер запросов в БД PostgreSQL.
    """

    def __init__(self, db):
        """
        Инициализация менеджера запросов.

        :param db: Экземпляр базы данных.
        :type db: gino.Gino
        """
        self.db = db

    async def save_query(
        self, user_id: int, product_code: str, timestamp: Optional[datetime] = None
    ) -> None:
        """
        Сохраняет запрос в базе данных.

        :param user_id: ID пользователя в телеграм.
        :type user_id: int
        :param product_code: Код продукта.
        :type product_code: str
        :param timestamp: Временная метка запроса. По умолчанию None.
        :type timestamp: Optional[datetime.datetime]
        :return: None
        """
        if timestamp is None:
            timestamp = datetime.now()
        await Query.create(
            user_id=user_id, timestamp=timestamp, product_code=product_code
        )

    async def get_latest_query_by_user_id(self, user_id: int) -> Optional[str]:
        """
        Получает последний запрос пользователя из базы данных.

        :param user_id: ID пользователяв телеграм.
        :type user_id: int
        :return: Код продукта последнего запроса пользователя или None, если запросов нет.
        :rtype: Optional[str]
        """
        query = (
            select(Query)
            .where(Query.user_id == user_id)
            .order_by(Query.timestamp.desc())
            .limit(1)
        )
        latest_query = await self.db.first(query)
        if latest_query:
            return latest_query.product_code
        else:
            return None


query_manager = QueryManager(db_instance)
