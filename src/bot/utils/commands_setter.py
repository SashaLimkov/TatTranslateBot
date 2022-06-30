from aiogram import types

from bot.config.loader import bot


async def set_default_commands():
    await bot.set_my_commands([
        types.BotCommand("/start", "Начать"),
    ])


async def delete_default_commands():
    await bot.delete_my_commands()
