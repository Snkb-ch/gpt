from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(ExamText)
admin.site.register(UniqueText)
admin.site.register(Order)
admin.site.register(User)
admin.site.register(Contact_us)
admin.site.register(PromoCode)
admin.site.register(PromoCodeUsage)


