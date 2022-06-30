import random

from aiogram import types
from aiogram.dispatcher import FSMContext

from app.models import GoogleTranslate, TatsoftTranslate, YandexTranslate, OriginalString
from bot.config.loader import bot, user_data
from bot.handlers.user.commands import new_message
from bot.services.db import translate
from bot.keyboards import inline as ik
from bot.states import UserState


async def second_q(call: types.CallbackQuery):
    original = await add_score_by_key(call)
    yandex, tatsoft, google = await translate.get_translates_by_original(original)
    yandex_translate: YandexTranslate = yandex
    google_translate: GoogleTranslate = google
    tatsoft_translate: TatsoftTranslate = tatsoft
    text = f"Какой перевод для данного предожения лучше?\n<b>{original.string}</b>\n\n"
    if yandex_translate.translate != tatsoft_translate.translate:
        translations = {"Y": yandex_translate, "T": tatsoft_translate}
        text += f"1){yandex_translate.translate}\n2){tatsoft_translate.translate}"
        await UserState.second.set()
        await new_message(call.message, translations, text)
    else:
        translations = {"G": google_translate, "T": tatsoft_translate}
        text += f"1){google_translate.translate}\n2){tatsoft_translate.translate}"
        await UserState.third.set()
        await new_message(call.message, translations, text)

    translations = {"Y": yandex_translate, "T": tatsoft_translate}
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=await ik.get_one_or_two(translations)
    )


async def third_q(call: types.CallbackQuery):
    original = await add_score_by_key(call)
    await UserState.third.set()
    google_translate: GoogleTranslate = await translate.get_google_translate_by_original(original)
    tatsoft_translate: TatsoftTranslate = await translate.get_tatsoft_translate_by_original(original)
    if tatsoft_translate.translate != google_translate.translate:
        text = f"Какой перевод для данного предожения лучше?\n<b>{original.string}</b>\n\n"
        translations = {"G": google_translate, "T": tatsoft_translate}
        text += f"1){google_translate.translate}\n2){tatsoft_translate.translate}"
        await new_message(call.message, translations, text)
    else:
        await finish(call)


async def finish(call: types.CallbackQuery):
    original = await add_score_by_key(call)
    await correct_score(original)
    first_score = await translate.get_score_of_first_batch()
    if first_score >= 200:
        batch = await translate.get_first_batch_of_originals()
    else:
        batch = await translate.get_all_originals()
    original: OriginalString = batch[0]
    yandex_translate: YandexTranslate = await translate.get_yandex_translate_by_original(original)
    google_translate: GoogleTranslate = await translate.get_google_translate_by_original(original)
    text = f"Какой перевод для данного предожения лучше?\n<b>{original.string}</b>\n\n"
    text += f"1){google_translate.translate}\n2){yandex_translate.translate}"
    translations = {"G": google_translate, "Y": yandex_translate}
    await UserState.first.set()
    await new_message(call.message, translations, text=text)


async def stop(call: types.CallbackQuery):
    # user_data[call.message.chat.id]["mes_to_del"] = call.message.message_id
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Вы завершили опрос, напишите /start чтобы начать новый",
    )


async def add_score_by_key(call: types.CallbackQuery):
    translation = call.data.split("_")
    key = translation[0]
    if key == "G":
        print("google + 1")
        g_translation: GoogleTranslate = await translate.get_google_translate_by_id(translation[1])
        original = g_translation.original
        await translate.update_google_score(translation[1], g_translation.google_score + 1)
    elif key == "T":
        print("tatsoft + 1")
        t_translation: TatsoftTranslate = await translate.get_tatsoft_translate_by_id(translation[1])
        original = t_translation.original
        await translate.update_tatsoft_score(translation[1], t_translation.tatsoft_score + 1)
    else:
        print("yandex + 1")
        y_translation: YandexTranslate = await translate.get_yandex_translate_by_id(translation[1])
        original = y_translation.original
        await translate.update_yandex_score(translation[1], y_translation.yandex_score + 1)

    return original


async def correct_score(original):
    yandex, tatsoft, google = await translate.get_translates_by_original(original)
    yandex_translate: YandexTranslate = yandex
    google_translate: GoogleTranslate = google
    tatsoft_translate: TatsoftTranslate = tatsoft
    if yandex_translate.translate == google_translate.translate:
        y, g = yandex_translate.yandex_score, google_translate.google_score
        r = max(y, g)
        await translate.update_yandex_score(yandex_translate.pk, r)
        await translate.update_google_score(google_translate.pk, r)
    if google_translate.translate == tatsoft_translate.translate:
        t, g = tatsoft_translate.tatsoft_score, google_translate.google_score
        r = max(t, g)
        await translate.update_tatsoft_score(tatsoft_translate.pk, r)
        await translate.update_google_score(google_translate.pk, r)
    if tatsoft_translate.translate == yandex_translate.translate:
        t, y = tatsoft_translate.tatsoft_score, yandex_translate.yandex_score
        r = max(t, y)
        await translate.update_tatsoft_score(tatsoft_translate.pk, r)
        await translate.update_yandex_score(yandex_translate.pk, r)
    await translate.update_original_score(original)
