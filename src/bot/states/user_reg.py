from aiogram.dispatcher.filters.state import StatesGroup, State


class UserRegistration(StatesGroup):
    registration = State()
    sex = State()
    age = State()
    education = State()
    skill = State()
    fio = State()
