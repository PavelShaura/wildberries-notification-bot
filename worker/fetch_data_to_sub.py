import aiohttp
from config.config import redis_client
from typing import Optional


async def fetch_and_send_product_info(article: str, user_id: int) -> Optional[str]:
    """
    Получает информацию о товаре по его артикулу и отправляет сообщение пользователю с информацией:
    Название, артикул, цена, рейтинг товара, количество товара НА ВСЕХ СКЛАДАХ.

    :param article: Артикул товара.
    :type article: str
    :param user_id: Идентификатор пользователя.
    :type user_id: int
    :return: Сообщение с информацией о товаре.
    :rtype: Optional[str]
    """
    async with aiohttp.ClientSession() as session:
        url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article}"
        async with session.get(url) as response:
            product_info = await response.json()

    if product_info:
        product_data = product_info.get("data", {}).get("products", [])
        if product_data:
            product = product_data[0]
            name = product.get("name")
            article = article
            price = product.get("salePriceU")
            rating = product.get("reviewRating")
            rating = rating if rating >= 0.1 else "Нет оценок"
            quantity = sum(
                stock.get("qty", 0)
                for size in product.get("sizes", [])
                for stock in size.get("stocks", [])
            )

            rub, kop = divmod(price, 100)
            price_formatted = f"<code>{rub}</code> руб. <code>{kop:02d}</code> коп."

            message = (
                f"📌  <i>Название</i>:    <b>{name}</b>\n "
                f"🔢  <i>Артикул</i>:    <code>{article}</code>\n "
                f"📈  <i>Цена</i>:    {price_formatted}\n "
                f"🏅  <i>Рейтинг товара</i>:    <code>{rating}</code> \n "
                f"🔍  <i>Количество товара на всех складах</i>:   <code>{quantity}</code>"
            )

            await redis_client.add_user_message(user_id, message)
            return message
