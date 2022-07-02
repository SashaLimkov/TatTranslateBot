from aiogram import Dispatcher
from aiogram.dispatcher import filters

from bot.filters.admin import AdminFilter
from bot.handlers.admin import init_db


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
    dp.register_message_handler(
        init_db.init_db, filters.Command("init_db"), is_admin=True
    )
    # dp.register_message_handler(cleaner.clean_s)
