from aiogram import Dispatcher
from aiogram.dispatcher import filters
import user_registration
from bot.states import UserRegistration
from bot.data import callback_data as cd


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(user_registration.start_register_client, cd.reg.filter(),
                                       state=UserRegistration.registration)
    dp.register_callback_query_handler(user_registration.get_sex, filters.Text(startswith="sex_"),
                                       state=UserRegistration.registration)
    dp.register_message_handler(user_registration.get_height, state=UserRegistration.education)
    dp.register_message_handler(user_registration.get_weight, state=UserRegistration.skill)
    dp.register_message_handler(user_registration.get_fio, state=UserRegistration.fio)
    dp.register_message_handler(user_registration.get_age, state=UserRegistration.age)
