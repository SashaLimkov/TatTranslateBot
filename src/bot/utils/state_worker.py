from aiogram.dispatcher import FSMContext


async def get_info_from_state(data, key):
    return data[key] if key in list(data.keys()) else ""
