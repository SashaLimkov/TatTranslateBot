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


class User(TimeBasedModel):
    class Meta:
        verbose_name = "Зарегестрированный пользоваетель"
        verbose_name_plural = "Зарегестрированные пользоваетели"

    tg_user = models.OneToOneField(TelegramUser,
                                   related_name="user",
                                   on_delete=models.CASCADE,
                                   verbose_name="Зарегестрированный Пользователь",
                                   )
    age = models.CharField(max_length=1, verbose_name="Возраст", )
    sex = models.IntegerField(verbose_name="Гендер")
    education = models.CharField(max_length=255, verbose_name="Уровень образования")
    skill = models.CharField(max_length=255, verbose_name="Уровень знания языка")


class OriginalString(TimeBasedModel):
    class Meta:
        verbose_name = "Оригинал строки"
        verbose_name_plural = "Оригиналы строк"

    def __str__(self):
        return self.string

    string = models.CharField(
        max_length=200, unique=True, verbose_name="Оригинальная строка"
    )
    length = models.IntegerField(verbose_name="Длинна строки")
    rates = models.IntegerField(verbose_name="Сумма балов", default=0)


class TatsoftTranslate(TimeBasedModel):
    class Meta:
        verbose_name = "Первеод от Tatsoft"
        verbose_name_plural = "Переводы от Tatsoft"

    original = models.OneToOneField(
        OriginalString,
        related_name="get_tatsoft",
        on_delete=models.CASCADE,
        verbose_name="Оригинал",
    )
    translate = models.CharField(
        max_length=200, unique=False, verbose_name="Перевод от Tatsoft"
    )
    length = models.IntegerField(verbose_name="Длинна строки")
    tatsoft_score = models.IntegerField(verbose_name="Баллы Tatsoft")


class YandexTranslate(TimeBasedModel):
    class Meta:
        verbose_name = "Первеод от Yandex"
        verbose_name_plural = "Переводы от Yandex"

    original = models.OneToOneField(
        OriginalString,
        related_name="get_yandex",
        on_delete=models.CASCADE,
        verbose_name="Оригинал",
    )
    translate = models.CharField(
        max_length=200, unique=False, verbose_name="Перевод от Yandex"
    )
    length = models.IntegerField(verbose_name="Длинна строки")
    yandex_score = models.IntegerField(verbose_name="Баллы Yandex")


class GoogleTranslate(TimeBasedModel):
    class Meta:
        verbose_name = "Первеод от Google"
        verbose_name_plural = "Переводы от Google"

    original = models.OneToOneField(
        OriginalString,
        related_name="get_google",
        on_delete=models.CASCADE,
        verbose_name="Оригинал",
    )
    translate = models.CharField(
        max_length=200, unique=False, verbose_name="Перевод от Google"
    )
    length = models.IntegerField(verbose_name="Длинна строки")
    google_score = models.IntegerField(verbose_name="Баллы Google")


class FirstBatch(TimeBasedModel):
    class Meta:
        verbose_name = "Первоочередный Оригинал"
        verbose_name_plural = "Первоочередные Оригиналы"

    def __str__(self):
        return self.original.string

    original = models.OneToOneField(
        OriginalString,
        on_delete=models.CASCADE,
        verbose_name="Оригинал",
    )


class UserAnswers(TimeBasedModel):
    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователя"

    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name="get_answers",
        verbose_name="Телеграм Пользователь",
    )
    original = models.ForeignKey(
        OriginalString, on_delete=models.CASCADE, verbose_name="Оригинал строки"
    )
