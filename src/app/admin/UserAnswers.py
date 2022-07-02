from django.contrib import admin

from app.models import UserAnswers


class UserAnswersAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "original",
        "created_at",
        "updated_at",
    )
    search_fields = ["original", "user"]
    ordering = ["-updated_at"]


admin.site.register(UserAnswers, UserAnswersAdmin)
