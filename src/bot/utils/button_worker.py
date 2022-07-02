from aiogram.types import InlineKeyboardButton


async def add_button(text: str, cd: str = None, url: str = None):
    return (
        InlineKeyboardButton(text=text, url=url)
        if url
        else InlineKeyboardButton(
            text=text,
            callback_data=cd,
        )
    )
