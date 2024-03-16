from db.database import db
from datetime import datetime


class Query(db.Model):
    """
    Модель запроса к базе данных PostgreSQL.
    """

    __tablename__ = 'queries'

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.BigInteger)
    timestamp: datetime = db.Column(db.DateTime)
    product_code: str = db.Column(db.String)

    def __init__(self, user_id: int, timestamp: datetime, product_code: str, **kwargs) -> None:
        """
        Инициализатор объекта запроса.

        :param user_id: ID пользователя в телеграм.
        :type user_id: int
        :param timestamp: Временная метка запроса.
        :type timestamp: datetime.datetime
        :param product_code: Код продукта.
        :type product_code: str
        :param kwargs: Дополнительные аргументы.
        """
        super().__init__(**kwargs)
        self.__values__.update(kwargs)
        self.user_id = user_id
        self.timestamp = timestamp
        self.product_code = product_code
