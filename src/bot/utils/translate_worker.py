from app.models import (
    YandexTranslate,
    GoogleTranslate,
    TatsoftTranslate,
    OriginalString,
)
from bot.services.db import translate as translate_db


async def get_translates(original):
    yandex, tatsoft, google = await translate_db.get_translates_by_original(original)
    return yandex, tatsoft, google


async def get_translations_dict(
    yandex: YandexTranslate, tatsoft: TatsoftTranslate, google: GoogleTranslate
):
    if yandex.translate == tatsoft.translate:
        return {"Q": {"Y": yandex, "G": google}, "C": 1}
    elif yandex.translate == google.translate:
        return {"Q": {"Y": yandex, "T": tatsoft}, "C": 1}
    elif tatsoft.translate == google.translate:
        return {"Q": {"G": google, "Y": yandex}, "C": 1}
    else:
        return {"Q": {"G": google, "Y": yandex, "T": tatsoft}, "C": 3}
