from aiogram.types import InlineKeyboardMarkup

__all__ = ["get_one_or_two"]

from bot.utils.button_worker import add_button


async def get_one_or_two(translations: dict, original):
    keyboard = InlineKeyboardMarkup(row_width=2)
    first_key, second_key = translations.keys()
    a = [first_key, second_key]
    keyboard.insert(await add_button(text="1️⃣", cd=f"{a[0]}_{translations[a[0]].id}"))
    keyboard.insert(await add_button(text="2️⃣", cd=f"{a[1]}_{translations[a[1]].id}"))

    keyboard.insert(
        await add_button(
            text="Одинаково хорошо",
            cd=f"sc_{first_key}_{translations[first_key].id}_{second_key}_{translations[second_key].id}",
        )
    )
    keyboard.insert(
        await add_button(
            text="Одинаково плохо",
            cd=f"sb_{original.pk}",
        )
    )
    keyboard.add(await add_button(text="Завершить", cd=f"stop"))
    return keyboard
