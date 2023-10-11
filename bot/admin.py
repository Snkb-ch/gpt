from django.contrib import admin

# Register your models here.



from .models import *

from django.contrib import admin

from django import forms




class MultiDBModelAdmin(admin.ModelAdmin):


    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.

        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.

        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

class BotAdmin(MultiDBModelAdmin):
    using = 'bottg'



admin.site.register(Subscriptions, BotAdmin)

admin.site.register(Statistics_by_day, BotAdmin)

admin.site.register(Subscriptions_statistics, BotAdmin)
admin.site.register(AnalyticsForDay, BotAdmin)

class CustomSearchFields(admin.SimpleListFilter):
    title = 'Для Поиска по полям'
    parameter_name = 'search_field'

    def lookups(self, request, model_admin):
        return (
            ('user_id', 'User ID'),
            ('email', 'Email'),
            ('sub_type__sub_name', 'Subscription Type'),
            ('last_message', 'Last Message'),
            ('time_sub', 'Subscription Time'),

        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                **{f'{self.value()}__icontains': request.GET.get('q', '')}
            )
        return queryset

class UserAdmin(BotAdmin, admin.ModelAdmin):

    list_display = ('user_id', 'status', 'used_tokens', 'time_sub', 'end_time', 'sub_type', 'email', 'last_message', 'utm_source', 'utm_campaign','model', 'admin', 'blocked',  'phrase_id', 'device_type', 'ad_id')
    list_filter = ('status', 'sub_type', 'blocked', CustomSearchFields)
    search_fields = ('user_id', 'email', 'last_message', 'time_sub')

admin.site.register(User, UserAdmin)


