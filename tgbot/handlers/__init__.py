from tgbot.handlers.start import command_start_router
from tgbot.handlers.send_product_info import get_product_router
from tgbot.handlers.subscribe import subscribe_router
from tgbot.handlers.database_info import database_info_router
from tgbot.handlers.unsubscribe import unsubscribe_router
from tgbot.handlers.unexpected import unexpected_message_router

routers = [
    subscribe_router,
    database_info_router,
    unsubscribe_router,
    command_start_router,
    get_product_router,
    unexpected_message_router,
]
