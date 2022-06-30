from django.contrib import admin
from django.utils.safestring import mark_safe

from ..models import TelegramUser, OriginalString, TatsoftTranslate, YandexTranslate, GoogleTranslate


class UsersAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "name",
        "user_rate",
        "created_at",
        "updated_at",
    )


class OriginalAdmin(admin.ModelAdmin):
    list_display = (
        "string",
        "rates",
        "yandex",
        "tatsoft",
        "google",
        "length",
        "created_at",
        "updated_at"
    )
    search_fields = ["string"]
    ordering = ["-rates"]

    def yandex(self, obj):
        return mark_safe(
            u'<a href="/admin/app/yandextranslate/%s/change/">%s</a>' % (obj.get_yandex.pk, obj.get_yandex.translate))

    def tatsoft(self, obj):
        return mark_safe(
            u'<a href="/admin/app/tatsofttranslate/%s/change/">%s</a>' % (
                obj.get_tatsoft.pk, obj.get_tatsoft.translate))

    def google(self, obj):
        return mark_safe(
            u'<a href="/admin/app/googletranslate/%s/change/">%s</a>' % (obj.get_google.pk, obj.get_google.translate))

    def __init__(self, *args, **kwargs):
        super(OriginalAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = ("yandex", "google", "tatsoft", "string")


class YandexAdmin(admin.ModelAdmin):
    list_display = (
        "original_link",
        "translate",
        "length",
        "yandex_score",
        "updated_at"
    )
    ordering = ["-yandex_score"]
    search_fields = ["translate"]

    def original_link(self, obj):
        return mark_safe(
            u'<a href="/admin/app/originalstring/%s/change/">%s</a>' % (obj.original.pk, obj.original.string))

    def __init__(self, *args, **kwargs):
        super(YandexAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = ("original_link", "translate")


class GoogleAdmin(admin.ModelAdmin):
    list_display = (
        "original_link",
        "translate",
        "length",
        "google_score",
        "updated_at"
    )

    search_fields = ["translate"]
    ordering = ["-google_score"]
    def original_link(self, obj):
        return mark_safe(
            u'<a href="/admin/app/originalstring/%s/change/">%s</a>' % (obj.original.pk, obj.original.string))

    def __init__(self, *args, **kwargs):
        super(GoogleAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = ("original_link", "translate")


class TatsoftAdmin(admin.ModelAdmin):
    list_display = (
        "original_link",
        "translate",
        "length",
        "tatsoft_score",
        "updated_at"
    )
    search_fields = ["translate"]
    ordering = ["-tatsoft_score"]
    def original_link(self, obj):
        return mark_safe(
            u'<a href="/admin/app/originalstring/%s/change/">%s</a>' % (obj.original.pk, obj.original.string))

    def __init__(self, *args, **kwargs):
        super(TatsoftAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = ("original_link", "translate")


# Register your models here.
admin.site.register(TelegramUser, UsersAdmin)
admin.site.register(OriginalString, OriginalAdmin)
admin.site.register(YandexTranslate, YandexAdmin)
admin.site.register(TatsoftTranslate, TatsoftAdmin)
admin.site.register(GoogleTranslate, GoogleAdmin)
