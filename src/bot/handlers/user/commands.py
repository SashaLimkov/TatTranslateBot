import random

from aiogram import types

from app.models import OriginalString, TatsoftTranslate, GoogleTranslate, YandexTranslate
from bot.config.loader import bot
from bot.states import UserState
from bot.utils import deleter
from bot.services.db import translate as translate_db
from bot.keyboards import inline as ik


async def start_cmd(message: types.Message):
    await deleter.delete_user_message(message)
    first_score = await translate_db.get_score_of_first_batch()
    if first_score >= 200:
        batch = await translate_db.get_first_batch_of_originals()
    else:
        batch = await translate_db.get_all_originals()
    original: OriginalString = batch[0]
    yandex, tatsoft, google = await translate_db.get_translates_by_original(original)
    yandex_translate: YandexTranslate = yandex
    google_translate: GoogleTranslate = google
    tatsoft_translate: TatsoftTranslate = tatsoft
    text = f"Какой перевод для данного предожения лучше?\n<b>{original.string}</b>\n\n"
    if google_translate.translate != yandex_translate.translate:
        text += f"1){google_translate.translate}\n2){yandex_translate.translate}"
        translations = {"G": google_translate, "Y": yandex_translate}
        await UserState.first.set()
        await new_message(message, translations, text)
    elif yandex_translate.translate != tatsoft_translate.translate:
        translations = {"Y": yandex_translate, "T": tatsoft_translate}
        text += f"1){yandex_translate.translate}\n2){tatsoft_translate.translate}"
        await UserState.second.set()
        await new_message(message, translations, text)
    else:
        translations = {"G": google_translate, "T": tatsoft_translate}
        text += f"1){google_translate.translate}\n2){tatsoft_translate.translate}"
        await UserState.third.set()
        await new_message(message, translations, text)


async def new_message(message: types.Message, translations, text):
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text=text,
            reply_markup=await ik.get_one_or_two(translations)
        )
    except Exception as e:
        print(e)
        await bot.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=await ik.get_one_or_two(translations)
        )
