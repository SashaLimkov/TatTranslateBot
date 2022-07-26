from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe

from app.models import OriginalString


class OriginalAdmin(admin.ModelAdmin):
    list_display = (
        "string",
        "rates",
        "yandex",
        "y_score",
        "tatsoft",
        "t_score",
        "google",
        "g_score",
        "length",
        "created_at",
        "updated_at",
    )
    search_fields = ["string"]

    def yandex(self, obj):
        return mark_safe(
            '<a href="/admin/app/yandextranslate/%s/change/">%s</a>'
            % (obj.get_yandex.pk, obj.get_yandex.translate)
        )

    def y_score(self, obj):
        return f"{obj.get_yandex.yandex_score}"

    def tatsoft(self, obj):
        return mark_safe(
            '<a href="/admin/app/tatsofttranslate/%s/change/">%s</a>'
            % (obj.get_tatsoft.pk, obj.get_tatsoft.translate))

    def t_score(self, obj):
        return f"{obj.get_tatsoft.tatsoft_score}"

    def google(self, obj):
        return mark_safe(
            '<a href="/admin/app/googletranslate/%s/change/">%s</a>'
            % (obj.get_google.pk, obj.get_google.translate))

    def g_score(self, obj):
        return f"{obj.get_google.google_score}"

    def __init__(self, *args, **kwargs):
        super(OriginalAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = ("yandex", "google", "tatsoft", "string")
        self.ordering = ["-rates"]


admin.site.register(OriginalString, OriginalAdmin)
