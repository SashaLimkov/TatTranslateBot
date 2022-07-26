import random

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.config.loader import bot
from bot.keyboards import inline as ik
from bot.services.db import translate as translate_db
from bot.services.db import user as user_db
from bot.states import UserState
from bot.utils import deleter
from bot.utils.translate_worker import get_translates, get_translations_dict


async def start_cmd(message: types.Message, state: FSMContext):
    await deleter.delete_user_message(message)
    user_id = message.chat.id
    user = await user_db.get_user(user_id)
    if not user:
        user = await user_db.add_user(user_id, message.from_user.first_name)
    data = await state.get_data()
    if data:
        original_id = data.get("original")
        q = await translate_db.get_original(original_id)
    else:
        q = await get_new_q(user)
    await send_first_q(q, message, state)


async def new_message(message: types.Message, translations, text, original):
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text=text,
            reply_markup=await ik.get_one_or_two(translations, original),
        )
    except Exception as e:
        print(e)
        await bot.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=await ik.get_one_or_two(translations, original),
        )


async def get_new_q(user):
    user_answers = await user_db.get_user_answers(user)
    u_answers = [orig.original for orig in user_answers]
    first_batch = await translate_db.get_first_batch()
    if len(user_answers) < len(first_batch):
        q = random.choice(first_batch)
        while q.original in u_answers:
            print(1)
            q = random.choice(first_batch)
        return q.original
    else:
        originals = await translate_db.get_all_originals()
        q = random.choice(originals)
        while q in u_answers:
            q = random.choice(originals)
        return q


async def send_first_q(q, message, state: FSMContext):
    yandex, tatsoft, google = await get_translates(q)
    data = await get_translations_dict(yandex, tatsoft, google)
    text = f"Какой перевод для данного предложения лучше?\n\n<b>{q.string}</b>\n\n"
    if data["C"] == 1:
        for k, v in data["Q"].items():
            text += f"{list(data['Q'].keys()).index(k) + 1}){v.translate}\n"
        await UserState.third.set()
        await new_message(message, data["Q"], text, q)
    else:
        await UserState.first.set()
        text += f"1) {google.translate}\n2) {yandex.translate}"
        translations = {"G": data["Q"]["G"], "Y": data["Q"]["Y"]}
        await new_message(message, translations, text, q)
    await state.update_data({"original": q})
