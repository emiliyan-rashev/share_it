from django.contrib import admin

from users.models import User


class CustomUserAdmin(admin.ModelAdmin):
    fields = ("email", "first_name", "last_name", "payment_url", "avatar")


admin.site.register(User, CustomUserAdmin)
