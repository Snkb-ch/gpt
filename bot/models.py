from django.db import models

# Create your models here.
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class BotTGUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('bottg')


class Subscriptions(models.Model):
    sub_id = models.AutoField(primary_key=True)
    sub_name = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    max_tokens = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    edit_temp = models.BooleanField(default=False)
    edit_role = models.BooleanField(default=False)
    duration = models.IntegerField(null=True)
    temp = models.FloatField(null=True, default=1)
    for_sale = models.BooleanField(default=False)
    objects = BotTGUserManager()
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sub_id'], name='subscriptions_pkey'),
        ]

    def __str__(self):
        return str(self.sub_name)

class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=25, default='active', null=True)
    used_tokens = models.IntegerField(default=0, null=True)
    time_sub = models.DateField(auto_now_add=True, null=True)
    end_time = models.DateField(null=True)
    sub_type = models.ForeignKey(Subscriptions, on_delete=models.RESTRICT, null=True)
    custom_temp = models.FloatField(default=1, null=True)
    email = models.CharField(max_length=50, null=True)
    expired_date = models.DateField(null=True)
    admin = models.BooleanField(default=False, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id'], name='users_user_id_key'),
        ]
    objects = BotTGUserManager()

    def __str__(self):
        return str(self.user_id)


class Period(models.Model):
    id_period = models.AutoField(primary_key=True)
    begin = models.TimeField(null=True)
    end = models.TimeField(null=True)
    objects = BotTGUserManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id_period'], name='periods_pkey'),
        ]
        managed = 'bottg'

    def __str__(self):
        return str(self.id_period)



class AnalyticsForMonth(models.Model):
    id = models.AutoField(primary_key=True)
    sub_type = models.ForeignKey(Subscriptions, on_delete=models.CASCADE)
    begin_date = models.DateField()
    active = models.IntegerField(default=1)
    input_tokens = models.BigIntegerField(default=0)
    output_tokens = models.BigIntegerField(default=0)
    total_tokens = models.BigIntegerField(default=0)
    expired_time = models.IntegerField(default=0)
    expired_tokens = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)
    expired = models.IntegerField(default=0)
    income = models.IntegerField(default=0)
    temp_edited = models.IntegerField(default=0)
    role_edited = models.IntegerField(default=0)
    objects = BotTGUserManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sub_type', 'begin_date'], name='analytics_for_month_sub_type_beginning_key'),
        ]

    def __str__(self):
        return str(self.sub_type)
    # on create update previous month

@receiver(post_save, sender=AnalyticsForMonth)
def update_active_on_create(sender, instance, created, **kwargs):
     if created and AnalyticsForMonth.objects.filter(sub_type=instance.sub_type).count() > 1:

         previous_month = instance.begin_date[0:5] + str(int(instance.begin_date[5:7]) - 1) + instance.begin_date[7:]
         AnalyticsForMonth.objects.filter(sub_type=instance.sub_type, begin_date=previous_month).update(active=User.objects.filter(sub_type=instance.sub_type, status = 'active').count())


class AnalyticsPeriods(models.Model):
    id = models.AutoField(primary_key=True)
    sub_type = models.ForeignKey(Subscriptions, on_delete=models.CASCADE)
    month = models.DateField()
    day = models.CharField(max_length=20)
    period = models.IntegerField()
    tokens = models.BigIntegerField()
    users = models.IntegerField()

    objects = BotTGUserManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sub_type', 'day', 'month', 'period'], name='analytics_periods_sub_type_day_month_period_key'),
        ]

    def __str__(self):
        return str(self.sub_type)