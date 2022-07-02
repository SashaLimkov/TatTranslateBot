from django.contrib import admin
from django.utils.safestring import mark_safe

from app.models import FirstBatch


class FirstBatchAdmin(admin.ModelAdmin):
    list_display = (
        "original_link",
        "created_at",
        "updated_at",
    )

    def original_link(self, obj):
        return mark_safe(
            '<a href="/admin/app/originalstring/%s/change/">%s</a>'
            % (obj.original.pk, obj.original.string)
        )

    def __init__(self, *args, **kwargs):
        super(FirstBatchAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = ["original_link"]


admin.site.register(FirstBatch, FirstBatchAdmin)
