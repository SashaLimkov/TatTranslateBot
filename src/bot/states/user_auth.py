from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    first = State()
    second = State()
    third = State()
