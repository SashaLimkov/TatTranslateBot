from asgiref.sync import sync_to_async
from django.db.models import F
from app.models import (
    TelegramUser,
    OriginalString,
    YandexTranslate,
    TatsoftTranslate,
    GoogleTranslate,
    FirstBatch,
)


@sync_to_async
def add_original(string, str_lenght):
    try:
        r = OriginalString(string=string, length=str_lenght)
        r.save()
        return r
    except Exception as e:
        print(e)


@sync_to_async
def get_translates_by_original(original: OriginalString):
    yandex = original.get_yandex
    google = original.get_google
    tatsoft = original.get_tatsoft
    return yandex, tatsoft, google


@sync_to_async
def get_first_batch_of_originals():
    queryset = OriginalString.objects.filter().order_by("id")
    first_50 = queryset[:50].order_by("rates")
    return first_50


@sync_to_async
def get_all_originals():
    queryset = OriginalString.objects.filter().order_by("rates")
    return queryset


@sync_to_async
def get_score_of_first_batch():
    queryset = OriginalString.objects.filter().order_by("id")
    first_50 = queryset[:50]
    score = 0
    for obj in first_50:
        yandex = obj.get_yandex.yandex_score
        google = obj.get_google.google_score
        tatsoft = obj.get_tatsoft.tatsoft_score
        score += yandex + google + tatsoft
    return score


@sync_to_async
def add_yandex(original, translate, length):
    try:
        r = YandexTranslate(
            original=original, translate=translate, length=length, yandex_score=0
        )
        r.save()
        return r
    except Exception as e:
        print(e)


@sync_to_async
def get_yandex_translate_by_original(original):
    return YandexTranslate.objects.filter(original=original).first()


@sync_to_async
def get_yandex_translate_by_id(y_id):
    return YandexTranslate.objects.filter(id=y_id).first()


@sync_to_async
def add_tatsoft(original, translate, length):
    try:
        r = TatsoftTranslate(
            original=original, translate=translate, length=length, tatsoft_score=0
        )
        r.save()
        return r
    except Exception as e:
        print(e)


@sync_to_async
def get_tatsoft_translate_by_original(original):
    return TatsoftTranslate.objects.filter(original=original).first()


@sync_to_async
def get_tatsoft_translate_by_id(t_id):
    return TatsoftTranslate.objects.filter(id=t_id).first()


@sync_to_async
def add_google(original, translate, length):
    try:
        r = GoogleTranslate(
            original=original, translate=translate, length=length, google_score=0
        )
        r.save()
        return r
    except Exception as e:
        print(e)


@sync_to_async
def get_google_translate_by_original(original):
    return GoogleTranslate.objects.filter(original=original).first()


@sync_to_async
def get_google_translate_by_id(g_id):
    return GoogleTranslate.objects.filter(id=g_id).first()


@sync_to_async
def update_google_score(translate_id, score):
    return GoogleTranslate.objects.filter(id=translate_id).update(google_score=score)


@sync_to_async
def update_yandex_score(translate_id, score):
    YandexTranslate.objects.filter(pk=translate_id).update(yandex_score=score)



@sync_to_async
def update_tatsoft_score(translate_id, score):
    return TatsoftTranslate.objects.filter(pk=translate_id).update(tatsoft_score=score)


@sync_to_async
def update_original_score(o_id):
    orig = OriginalString.objects.filter(pk=o_id).first()
    yandex = orig.get_yandex.yandex_score
    google = orig.get_google.google_score
    tatsoft = orig.get_tatsoft.tatsoft_score
    rate = yandex + google + tatsoft
    return OriginalString.objects.filter(pk=o_id).update(rates=rate)


@sync_to_async
def get_first_batch():
    return FirstBatch.objects.all()

@sync_to_async
def get_original(o_id):
    return OriginalString.objects.filter(pk=o_id).first()