from aiogram.types import InlineKeyboardMarkup

__all__ = ["get_one_or_two", "main_menu", "setup_client", "gender"]

from bot.utils.button_worker import add_button
from bot.data import list_data as ld
from bot.data import callback_data as cd


async def main_menu():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(await add_button(text="Начать", cd="start"))
    keyboard.add(await add_button(text="Личный кабинет", cd="lk"))
    return keyboard


async def get_one_or_two(translations: dict, original):
    keyboard = InlineKeyboardMarkup(row_width=2)
    first_key, second_key = translations.keys()
    a = [first_key, second_key]
    keyboard.insert(await add_button(text="Первый лучше", cd=f"{a[0]}_{translations[a[0]].id}"))
    keyboard.insert(await add_button(text="Второй лучше", cd=f"{a[1]}_{translations[a[1]].id}"))

    keyboard.insert(
        await add_button(
            text="Оба хорошие",
            cd=f"sc_{first_key}_{translations[first_key].id}_{second_key}_{translations[second_key].id}",
        )
    )
    keyboard.insert(
        await add_button(
            text="Оба плохие",
            cd=f"sb_{original.pk}",
        )
    )
    keyboard.add(await add_button(text="Пропустить", cd=f"skip"))
    keyboard.add(await add_button(text="Завершить", cd=f"stop"))
    return keyboard


async def setup_client(data):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for index, text in enumerate(ld.REG_CLIENT):
        keyboard.add(
            await add_button(
                text=text,
                cd=cd.reg.new(
                    action=index + 1
                ))
        )
    if "age" in data and "sex" in data and "education" in data and "skill" in data:
        keyboard.add(
            await add_button(
                text="Подтвердить данные",
                cd=cd.reg.new(
                    action="submit"
                )
            )
        )
    return keyboard


async def gender():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        await add_button(text="Ж", cd="sex_g"),
        await add_button(text="М", cd="sex_m"),
    )
    return keyboard
