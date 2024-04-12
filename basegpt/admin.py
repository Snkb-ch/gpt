from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(ExamText)
admin.site.register(UniqueText)
admin.site.register(Order)

admin.site.register(Contact_us)
admin.site.register(PromoCode)
admin.site.register(PromoCodeUsage)
admin.site.register(Crawl)


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("email", "is_staff", "is_active", "friends", "code", "balance")
    list_filter = ("email", "is_staff", "is_active",  "friends", "code")
    fieldsets = (
        (None, {"fields": ("email", "password", "friends", "code")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
