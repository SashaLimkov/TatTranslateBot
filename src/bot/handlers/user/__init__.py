from aiogram import Dispatcher
from aiogram.dispatcher import filters

from bot.handlers.user import cleaner, commands, questions
from bot.states import UserState


def setup(dp: Dispatcher):
    dp.register_message_handler(commands.start_cmd, filters.CommandStart(), state="*")
    dp.register_callback_query_handler(questions.stop, filters.Text(equals="stop"), state="*")
    dp.register_callback_query_handler(questions.second_q, state=UserState.first)
    dp.register_callback_query_handler(questions.third_q, state=UserState.second)
    dp.register_callback_query_handler(questions.finish, state=UserState.third)
    dp.register_message_handler(cleaner.clean_s)
