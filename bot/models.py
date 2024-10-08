from django.db import models

# Create your models here.
from django.db import models
from django.db.models.deletion import Collector
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
    multimodel = models.BooleanField(default=False)
    multi_k = models.IntegerField(null=True)
    gen_im =  models.BooleanField(default=False)
    cost= models.FloatField(null=True, default=0)
    objects = BotTGUserManager()
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sub_id'], name='subscriptions_pkey'),
        ]

    def __str__(self):
        return str(self.sub_name) + ' ' + str('For sale' if self.for_sale else 'Archive')


class Models(models.Model):
    model_name_user = models.CharField(max_length=100, null=True)
    model_name  = models.CharField(max_length=100, null=True)
    max_tokens =  models.IntegerField(default=4096, null=True)
    model_k =  models.IntegerField(default=1, null=True)

    objects = BotTGUserManager()

    def __str__(self):
        return str(self.model_name_user) + str(self.model_k)

class Subscriptions_models(models.Model):
    sub = models.ForeignKey(Subscriptions, on_delete=models.CASCADE)
    model = models.ForeignKey(Models, on_delete=models.CASCADE)
    objects = BotTGUserManager()

    def __str__(self):
        return str(self.sub) + ' ' + str(self.model)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sub', 'model'], name='subscriptions_models_pkey'),
        ]



    

class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=25, default='active', null=True)
    used_tokens = models.IntegerField(default=0, null=True)
    time_sub = models.DateField(auto_now_add=True, null=True)
    end_time = models.DateField(null=True)
    sub_type = models.ForeignKey(Subscriptions, on_delete=models.RESTRICT, null=True)
    custom_temp = models.FloatField(default=1, null=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    # date to remind user about expiring subscription
    reminder_date = models.DateField(null=True, blank=True)
    last_message = models.DateField(null=True, blank=True)

    model = models.CharField(max_length=50, default='gpt-4mini', null=True)
    admin = models.BooleanField(default=False, null=True)
    blocked = models.BooleanField(default=False, null=True)

    utm_source = models.CharField(max_length=50, null=True, blank=True)
    utm_campaign = models.BigIntegerField(null=True, blank=True)

    group_id = models.BigIntegerField(null=True, blank=True)
    # utm_content
    client_id_metrika = models.BigIntegerField(null=True, blank=True)
    tg_channel_used = models.IntegerField(null=True, blank=True, default=0)
    poll_answers = models.TextField(null=True, blank=True)






    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id'], name='users_user_id_key'),
        ]
    objects = BotTGUserManager()


    def __str__(self):
        return str(self.user_id)



class Offline_conversions(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    target = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)

    objects = BotTGUserManager()


class Offline_conversions_settings(models.Model):
    id = models.AutoField(primary_key=True)
    target = models.CharField(max_length=50)

    day_max = models.IntegerField(default=0)
    day_count = models.IntegerField(default=0)
    day_last_reset = models.DateField(null=True)
    objects = BotTGUserManager()


class Subscriptions_statistics(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,  null=True)
    sub_type = models.ForeignKey(Subscriptions, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True)

    active = models.BooleanField(default=True)
    expired_reason = models.CharField(max_length=50, null=True)
    role_edited = models.IntegerField(default=0)
    temp_edited = models.IntegerField(default=0)
    photo_send = models.IntegerField(default=0)
    image_generated = models.IntegerField(default=0)
    order_id_payment = models.CharField(max_length=100, null=True)



    income = models.FloatField(null=True, default=0)
    objects = BotTGUserManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id'], name='subscriptions_statistics_pkey'),
        ]

class Subscriptions_statistics_model(models.Model):

    id = models.AutoField(primary_key=True)
    sub_stat = models.ForeignKey(Subscriptions_statistics, on_delete=models.SET_NULL ,  null=True)
    model = models.CharField(max_length=50)
    input_tokens = models.IntegerField(null=True, default=0)
    output_tokens = models.IntegerField(null=True, default=0)
    messages = models.IntegerField(null=True, default=0)

    objects = BotTGUserManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id'], name='subscriptions_statistics_model_pkey'),
        ]

class Statistics_by_day(models.Model):
    id = models.AutoField(primary_key=True)
    sub_stat = models.ForeignKey(Subscriptions_statistics, on_delete=models.SET_NULL ,  null=True)
    day = models.DateField()
    input_tokens = models.IntegerField(null=True, default=0)
    output_tokens = models.IntegerField(null=True, default=0)
    messages = models.IntegerField(null=True, default=0)
    costs = models.FloatField(null=True, default=0)



    objects = BotTGUserManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id'], name='statistics_by_day_pkey'),
        ]






class AdminStats(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    month = models.DateField()
    work_cost = models.FloatField(default=0)
    personal_cost = models.FloatField(default=0)
    type_now = models.CharField(max_length=50, null=True)
    objects = BotTGUserManager()


