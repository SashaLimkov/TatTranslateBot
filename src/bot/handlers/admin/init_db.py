from aiogram import types

from app.models import OriginalString
from bot.services.db import translate as t_db
from bot.services.gsheets.test import get_data


async def init_db(message: types.Message):
    print(111111111111)
    data = await get_data()
    for original in list(data.keys()):
        if original == "":
            continue
        r: OriginalString = await t_db.add_original(original, len(original))
        await t_db.add_tatsoft(
            r, data[original]["Tatsoft"], len(data[original]["Tatsoft"])
        )
        await t_db.add_yandex(
            r, data[original]["Yandex"], len(data[original]["Yandex"])
        )
        await t_db.add_google(
            r, data[original]["Google"], len(data[original]["Google"])
        )
