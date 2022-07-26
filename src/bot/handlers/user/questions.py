from aiogram import types
from aiogram.dispatcher import FSMContext

from app.models import (
    GoogleTranslate,
    TatsoftTranslate,
    YandexTranslate,
)
from bot.config.loader import bot
from bot.handlers.user.commands import new_message, get_new_q, send_first_q
from bot.services.db import translate as translate_db
from bot.services.db import user as user_db
from bot.states import UserState
from bot.utils.translate_worker import get_translates
from bot.keyboards import inline as ik

async def second_q(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    original = data.get("original")
    yandex, tatsoft, google = await get_translates(original)
    text = f"Какой перевод для данного предложения лучше?\n\n<b>{original.string}</b>\n\n"
    text += f"1) {yandex.translate}\n2) {tatsoft.translate}"
    translations = {"Y": yandex, "T": tatsoft}
    await state.update_data({"1": call.data})
    await UserState.second.set()
    await new_message(call, translations, text, original)


async def third_q(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    original = data.get("original")
    yandex, tatsoft, google = await get_translates(original)
    text = f"Какой перевод для данного предожения лучше?\n\n<b>{original.string}</b>\n\n"
    text += f"1) {tatsoft.translate}\n2) {google.translate}"
    translations = {"T": tatsoft, "G": google}
    await state.update_data({"2": call.data})
    await UserState.third.set()
    await new_message(call, translations, text, original)


async def finish(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data({"3": call.data})
    data = await state.get_data()
    val = list(data.values())
    original = data.get('original')
    for answer in val[2:]:
        await add_score_by_key(answer)
    await correct_score(original)
    user = await user_db.get_user(call.message.chat.id)
    await user_db.update_user_answers(user, original)
    q = await get_new_q(await user_db.get_user(call.message.chat.id))
    await send_first_q(q, call, state)


async def skip(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    original = data.get("original")
    user = await user_db.get_user(call.message.chat.id)
    await user_db.update_user_answers(user, original)
    q = await get_new_q(await user_db.get_user(call.message.chat.id))
    await send_first_q(q, call, state)


async def stop(call: types.CallbackQuery):
    await call.answer()
    await UserState.mm.set()
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        text="Текст меню",
        reply_markup=await ik.main_menu(),
        message_id=call.message.message_id,
    )


async def add_score_by_key(answer: str):
    if answer.startswith("sb"):
        pass
    elif answer.startswith("sc"):
        data = answer.split("_")
        first_key, second_key = data[1], data[3]
        first_id, second_id = data[2], data[4]
        p = {first_key: first_id, second_key: second_id}
        for k, v in p.items():
            if k == "G":
                g_translation: GoogleTranslate = await translate_db.get_google_translate_by_id(
                    v
                )
                await translate_db.update_google_score(
                    v, g_translation.google_score + 1
                )
            elif k == "T":
                t_translation: TatsoftTranslate = (
                    await translate_db.get_tatsoft_translate_by_id(v)
                )
                await translate_db.update_tatsoft_score(
                    v, t_translation.tatsoft_score + 1
                )
            elif k == "Y":
                y_translation: YandexTranslate = await translate_db.get_yandex_translate_by_id(
                    v
                )
                score = y_translation.yandex_score
                await translate_db.update_yandex_score(
                    v, score + 1
                )
    else:
        translation = answer.split("_")
        key = translation[0]
        if key == "G":
            g_translation: GoogleTranslate = await translate_db.get_google_translate_by_id(
                translation[1]
            )
            await translate_db.update_google_score(
                translation[1], g_translation.google_score + 1
            )
        elif key == "T":
            t_translation: TatsoftTranslate = (
                await translate_db.get_tatsoft_translate_by_id(translation[1])
            )
            await translate_db.update_tatsoft_score(
                translation[1], t_translation.tatsoft_score + 1
            )
        else:
            y_translation: YandexTranslate = await translate_db.get_yandex_translate_by_id(
                translation[1]
            )
            score = y_translation.yandex_score
            await translate_db.update_yandex_score(
                translation[1], score + 1
            )


async def correct_score(q):
    original = await translate_db.get_original(q.pk)
    yandex, tatsoft, google = await get_translates(original)
    if google.translate == tatsoft.translate:
        t, g = tatsoft.tatsoft_score, google.google_score
        r = max(t, g)
        await translate_db.update_tatsoft_score(tatsoft.pk, r)
        await translate_db.update_google_score(google.pk, r)
    elif yandex.translate == tatsoft.translate:
        y, t = yandex.yandex_score, tatsoft.tatsoft_score
        r = max(y, t)
        await translate_db.update_yandex_score(yandex.pk, r)
        await translate_db.update_tatsoft_score(tatsoft.pk, r)
    elif tatsoft.translate == google.translate:
        t, g = tatsoft.tatsoft_score, google.google_score
        r = max(t, g)
        await translate_db.update_tatsoft_score(tatsoft.pk, r)
        await translate_db.update_google_score(google.pk, r)
    await translate_db.update_original_score(q.pk)
