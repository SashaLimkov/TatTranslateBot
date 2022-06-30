from aiogram import Dispatcher
from bot.handlers import user, admin


def setup(dp: Dispatcher):
    admin.setup(dp)
    user.setup(dp)
