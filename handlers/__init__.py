from handlers.start import command_start_router
from handlers.send_product_info import get_product_router
from handlers.subscribe import subscribe_router
from handlers.database_info import database_info_router
from handlers.unsubscribe import unsubscribe_router
from handlers.unexpected import unexpected_message_router

routers = [
    subscribe_router,
    database_info_router,
    unsubscribe_router,
    command_start_router,
    get_product_router,
    unexpected_message_router,
]
