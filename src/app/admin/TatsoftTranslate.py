from django.contrib import admin
from django.utils.safestring import mark_safe

from app.models import TatsoftTranslate


class TatsoftAdmin(admin.ModelAdmin):
    list_display = (
        "original_link",
        "translate",
        "length",
        "tatsoft_score",
        "updated_at",
    )
    search_fields = ["translate"]
    ordering = ["-tatsoft_score"]

    def original_link(self, obj):
        return mark_safe(
            '<a href="/admin/app/originalstring/%s/change/">%s</a>'
            % (obj.original.pk, obj.original.string)
        )

    def __init__(self, *args, **kwargs):
        super(TatsoftAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = ("original_link", "translate")


admin.site.register(TatsoftTranslate, TatsoftAdmin)
