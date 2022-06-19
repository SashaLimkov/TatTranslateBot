from django.contrib import admin

from ..models import TelegramUser


class UsersAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "name",
        "user_rate",
        "created_at",
        "updated_at",
    )


# Register your models here.
admin.site.register(TelegramUser, UsersAdmin)
