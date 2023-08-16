from django.db import models

# Create your models here.
from django.db import models
class Subscription(models.Model):
    sub_id = models.AutoField(primary_key=True)
    sub_name = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    max_tokens = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    edit_temp = models.BooleanField(default=False)
    edit_role = models.BooleanField(default=False)
    duration = models.IntegerField(null=True)
    temp = models.IntegerField(default=1)
    for_sale = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sub_id'], name='subscriptions_pkey'),
        ]

    def __str__(self):
        return str(self.sub_name)

class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=25, default='active')
    used_tokens = models.IntegerField(default=0)
    time_sub = models.DateField(auto_now_add=True)
    end_time = models.DateField(null=True)
    sub_type = models.ForeignKey(Subscription, on_delete=models.RESTRICT)
    custom_temp = models.IntegerField(default=1)
    email = models.CharField(max_length=50, null=True)
    expired_date = models.DateField(null=True)
    admin = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id'], name='users_user_id_key'),
        ]

    def __str__(self):
        return str(self.user_id)


class Period(models.Model):
    id_period = models.AutoField(primary_key=True)
    begin = models.TimeField(null=True)
    end = models.TimeField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id_period'], name='periods_pkey'),
        ]
        managed = 'bottg'

    def __str__(self):
        return str(self.id_period)

class AnalyticsForMonth(models.Model):
    id = models.AutoField(primary_key=True)
    sub_type = models.ForeignKey(Subscription, on_delete=models.CASCADE)
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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sub_type', 'begin_date'], name='analytics_for_month_sub_type_beginning_key'),
        ]

    def __str__(self):
        return str(self.sub_type)

class AnalyticsPeriods(models.Model):
    id = models.AutoField(primary_key=True)
    sub_type = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    month = models.DateField()
    day = models.CharField(max_length=20)
    period = models.IntegerField()
    tokens = models.IntegerField()
    users = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sub_type', 'day', 'month', 'period'], name='analytics_periods_sub_type_day_month_period_key'),
        ]

    def __str__(self):
        return str(self.sub_type)
