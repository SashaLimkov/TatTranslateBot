from aiogram import types

from aiogram import types

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


async def second_q(call: types.CallbackQuery):
    original = await add_score_by_key(call)
    yandex, tatsoft, google = await get_translates(original)
    text = f"Какой перевод для данного предложения лучше?\n<b>{original.string}</b>\n\n"
    text += f"1){yandex.translate}\n2){tatsoft.translate}"
    translations = {"Y": yandex, "T": tatsoft}
    await UserState.second.set()
    await new_message(call.message, translations, text, original)


async def third_q(call: types.CallbackQuery):
    original = await add_score_by_key(call)
    yandex, tatsoft, google = await get_translates(original)
    text = f"Какой перевод для данного предожения лучше?\n<b>{original.string}</b>\n\n"
    text += f"1){tatsoft.translate}\n2){google.translate}"
    translations = {"T": tatsoft, "G": google}
    await UserState.third.set()
    await new_message(call.message, translations, text, original)


async def finish(call: types.CallbackQuery):
    original = await add_score_by_key(call)
    await correct_score(original)
    user = await user_db.get_user(call.message.chat.id)
    await user_db.update_user_answers(user, original)
    q = await get_new_q(await user_db.get_user(call.message.chat.id))
    await send_first_q(q, call.message)


async def stop(call: types.CallbackQuery):
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Вы завершили опрос, напишите /start чтобы начать новый",
    )


async def add_score_by_key(call: types.CallbackQuery):
    if call.data.startswith("sb"):
        data = call.data.split("_")
        original = await translate_db.get_original(data[1])
        return original
    elif call.data.startswith("sc"):
        data = call.data.split("_")
        first_key, second_key = data[1], data[3]
        first_id, second_id = data[2], data[4]
        p = {first_key: first_id, second_key: second_id}
        for k, v in p.items():
            if k == "G":
                g_translation: GoogleTranslate = await translate_db.get_google_translate_by_id(
                    v
                )
                original = g_translation.original
                await translate_db.update_google_score(
                    v, g_translation.google_score + 1
                )
            elif k == "T":
                t_translation: TatsoftTranslate = (
                    await translate_db.get_tatsoft_translate_by_id(v)
                )
                original = t_translation.original
                await translate_db.update_tatsoft_score(
                    v, t_translation.tatsoft_score + 1
                )
            elif k == "Y":
                y_translation: YandexTranslate = await translate_db.get_yandex_translate_by_id(
                    v
                )
                score = y_translation.yandex_score
                original = y_translation.original
                await translate_db.update_yandex_score(
                    v, score + 1
                )

    translation = call.data.split("_")
    key = translation[0]
    if key == "G":
        g_translation: GoogleTranslate = await translate_db.get_google_translate_by_id(
            translation[1]
        )
        original = g_translation.original
        await translate_db.update_google_score(
            translation[1], g_translation.google_score + 1
        )
    elif key == "T":
        t_translation: TatsoftTranslate = (
            await translate_db.get_tatsoft_translate_by_id(translation[1])
        )
        original = t_translation.original
        await translate_db.update_tatsoft_score(
            translation[1], t_translation.tatsoft_score + 1
        )
    elif key == "Y":
        y_translation: YandexTranslate = await translate_db.get_yandex_translate_by_id(
            translation[1]
        )
        score = y_translation.yandex_score
        original = y_translation.original
        await translate_db.update_yandex_score(
            translation[1], score + 1
        )

    return original


async def correct_score(q):
    original = await translate_db.get_original(q.pk)
    yandex, tatsoft, google = await get_translates(original)
    if google.translate == tatsoft.translate:
        print(2)
        t, g = tatsoft.tatsoft_score, google.google_score
        r = max(t, g)
        await translate_db.update_tatsoft_score(tatsoft.pk, r)
        await translate_db.update_google_score(google.pk, r)
    elif yandex.translate == tatsoft.translate:
        y, t = yandex.yandex_score, tatsoft.tatsoft_score
        r = max(y, t)
        print(y, t, r)
        await translate_db.update_yandex_score(yandex.pk, r)
        await translate_db.update_tatsoft_score(tatsoft.pk, r)
    elif tatsoft.translate == google.translate:
        t, g = tatsoft.tatsoft_score, google.google_score
        r = max(t, g)
        await translate_db.update_tatsoft_score(tatsoft.pk, r)
        await translate_db.update_google_score(google.pk, r)
    await translate_db.update_original_score(q.pk)
