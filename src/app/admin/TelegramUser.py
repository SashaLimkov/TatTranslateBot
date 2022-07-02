from django.contrib import admin

from ..models import TelegramUser


class TelegramUsersAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "name",
        "created_at",
        "updated_at",
    )


# Register your models here.
admin.site.register(TelegramUser, TelegramUsersAdmin)
