from django.db import models


# Create your models here.
class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(auto_now=True)


class TelegramUser(TimeBasedModel):
    """
    Пользователь телеграма и его контактные данные
    """

    class Meta:
        verbose_name = "Телеграм Юзер"
        verbose_name_plural = "Телеграм Юзеры"

    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(unique=True, verbose_name="UserID")
    name = models.CharField(max_length=255, verbose_name="Telegram Имя пользователя")
    user_rate = models.IntegerField(verbose_name="Рейтинг пользователя")


class OriginalString(TimeBasedModel):
    class Meta:
        verbose_name = "Оригинал строки"
        verbose_name_plural = "Оригиналы строк"

    id = models.AutoField(primary_key=True)
    string = models.CharField(unique=True, verbose_name="Оригинальная строка")
    length = models.IntegerField(verbose_name="Длинна строки")


class TatsoftTranslate(TimeBasedModel):
    class Meta:
        verbose_name = "Первеод от Tatsoft"
        verbose_name_plural = "Переводы от Tatsoft"

    id = models.AutoField(primary_key=True)
    original_string_id = models.ForeignKey(OriginalString,
                                           on_delete=models.CASCADE,
                                           verbose_name="Оригинал",
                                           unique=True)
    translate = models.CharField(unique=True, verbose_name="Перевод от Tatsoft")
    length = models.IntegerField(verbose_name="Длинна строки")
    tatsoft_score = models.IntegerField(verbose_name="Баллы Tatsoft")


class YandexTranslate(TimeBasedModel):
    class Meta:
        verbose_name = "Первеод от Yandex"
        verbose_name_plural = "Переводы от Yandex"

    id = models.AutoField(primary_key=True)
    original_string_id = models.ForeignKey(OriginalString,
                                           on_delete=models.CASCADE,
                                           verbose_name="Оригинал",
                                           unique=True)
    translate = models.CharField(unique=True, verbose_name="Перевод от Yandex")
    length = models.IntegerField(verbose_name="Длинна строки")
    yandex_score = models.IntegerField(verbose_name="Баллы Yandex")


class GoogleTranslate(TimeBasedModel):
    class Meta:
        verbose_name = "Первеод от Google"
        verbose_name_plural = "Переводы от Google"

    id = models.AutoField(primary_key=True)
    original_string_id = models.ForeignKey(OriginalString,
                                           on_delete=models.CASCADE,
                                           verbose_name="Оригинал",
                                           unique=True)
    translate = models.CharField(unique=True, verbose_name="Перевод от Google")
    length = models.IntegerField(verbose_name="Длинна строки")
    google_score = models.IntegerField(verbose_name="Баллы Google")

#
# class TatsoftVsYandex(TimeBasedModel):
#     id = models.AutoField(primary_key=True)
#     original_string = models.ForeignKey(
#         OriginalString,
#         on_delete=models.CASCADE,
#         verbose_name="Оригинал",
#         unique=True
#     )
#     tatsoft_translate = models.ForeignKey(
#         TatsoftTranslate,
#         on_delete=models.CASCADE,
#         verbose_name="Перевод от Tatsoft",
#         unique=True
#     )
#     yandex_tranlate = models.ForeignKey(
#         YandexTranslate,
#         on_delete=models.CASCADE,
#         verbose_name="Перевод от Yandex",
#         unique=True
#     )
#
#
# class TatsoftVsGoogle(TimeBasedModel):
#     id = models.AutoField(primary_key=True)
#     original_string = models.ForeignKey(
#         OriginalString,
#         on_delete=models.CASCADE,
#         verbose_name="Оригинал",
#         unique=True
#     )
#     tatsoft_translate = models.ForeignKey(
#         TatsoftTranslate,
#         on_delete=models.CASCADE,
#         verbose_name="Перевод от Tatsoft",
#         unique=True
#     )
#     google_tranlate = models.ForeignKey(
#         YandexTranslate,
#         on_delete=models.CASCADE,
#         verbose_name="Перевод от Google",
#         unique=True
#     )
#
#
# class GoogleVsYandex(TimeBasedModel):
#     id = models.AutoField(primary_key=True)
#     original_string = models.ForeignKey(
#         OriginalString,
#         on_delete=models.CASCADE,
#         verbose_name="Оригинал",
#         unique=True
#     )
#     google_translate = models.ForeignKey(
#         TatsoftTranslate,
#         on_delete=models.CASCADE,
#         verbose_name="Перевод от Google",
#         unique=True
#     )
#     yandex_tranlate = models.ForeignKey(
#         YandexTranslate,
#         on_delete=models.CASCADE,
#         verbose_name="Перевод от Yandex",
#         unique=True
#     )

#
# class UserAnswers(TimeBasedModel):
#     user = models.ForeignKey(
#         TelegramUser,
#         on_delete=models.CASCADE,
#         verbose_name="Пользователь",
#         unique=True
#     )
#     string_id = models.ForeignKey(
#         OriginalString,
#         on_delete=models.CASCADE,
#         verbose_name="Ответ на сравнение с данной строкой",
#     )
#     score_to = models.
