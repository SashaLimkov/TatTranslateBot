from django.db import models


# Create your models here.
class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")


class TelegramUser(TimeBasedModel):
    """
    Пользователь телеграма и его контактные данные
    """

    class Meta:
        verbose_name = "Телеграм Юзер"
        verbose_name_plural = "Телеграм Юзеры"

    user_id = models.BigIntegerField(unique=True, verbose_name="UserID")
    name = models.CharField(max_length=255, verbose_name="Telegram Имя пользователя")
    user_rate = models.IntegerField(verbose_name="Рейтинг пользователя")


class OriginalString(TimeBasedModel):
    class Meta:
        verbose_name = "Оригинал строки"
        verbose_name_plural = "Оригиналы строк"

    def __str__(self):
        return self.string

    string = models.CharField(max_length=200, unique=True, verbose_name="Оригинальная строка")
    length = models.IntegerField(verbose_name="Длинна строки")
    rates = models.IntegerField(verbose_name="Сумма балов", default=0)


class TatsoftTranslate(TimeBasedModel):
    class Meta:
        verbose_name = "Первеод от Tatsoft"
        verbose_name_plural = "Переводы от Tatsoft"

    original = models.OneToOneField(OriginalString, related_name="get_tatsoft", on_delete=models.CASCADE,
                                    verbose_name="Оригинал")
    translate = models.CharField(max_length=200, unique=False, verbose_name="Перевод от Tatsoft")
    length = models.IntegerField(verbose_name="Длинна строки")
    tatsoft_score = models.IntegerField(verbose_name="Баллы Tatsoft")


class YandexTranslate(TimeBasedModel):
    class Meta:
        verbose_name = "Первеод от Yandex"
        verbose_name_plural = "Переводы от Yandex"

    original = models.OneToOneField(OriginalString, related_name="get_yandex", on_delete=models.CASCADE,
                                    verbose_name="Оригинал")
    translate = models.CharField(max_length=200, unique=False, verbose_name="Перевод от Yandex")
    length = models.IntegerField(verbose_name="Длинна строки")
    yandex_score = models.IntegerField(verbose_name="Баллы Yandex")


class GoogleTranslate(TimeBasedModel):
    class Meta:
        verbose_name = "Первеод от Google"
        verbose_name_plural = "Переводы от Google"

    original = models.OneToOneField(OriginalString, related_name="get_google", on_delete=models.CASCADE,
                                    verbose_name="Оригинал")
    translate = models.CharField(max_length=200, unique=False, verbose_name="Перевод от Google")
    length = models.IntegerField(verbose_name="Длинна строки")
    google_score = models.IntegerField(verbose_name="Баллы Google")
