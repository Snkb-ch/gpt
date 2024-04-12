import math

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
import os
from django.contrib.auth.models import AbstractUser
import uuid

import random
import string
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    balance = models.FloatField(default=0)


    email_verified = models.BooleanField(default=False)

    code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    friends = models.IntegerField(default=0)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email


    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_promo_code()

        super().save(*args, **kwargs)

    def generate_promo_code(self):
        length = 6
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
            if not PromoCode.objects.filter(code=code).exists():
                PromoCode.objects.create(code=code, discount=10, max_uses=math.inf)
                return code

    pass



class OrderTokens(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(null=True)
    tokens = models.IntegerField(null=True)
    transaction_id = models.CharField(max_length=100, null=True)
    complete = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    result = models.TextField(null=True)
    user_rating = models.IntegerField(null=True)
    all_count = models.IntegerField(null=True)
    raw_all_count = models.IntegerField(null=True)




    procent = models.IntegerField(null=True)
    rating = models.IntegerField(null=True)
    raw_procent = models.IntegerField(null=True)
    raw_rating = models.IntegerField(null=True)


    loops = models.IntegerField(null=True)
    textv1 = models.TextField(null=True)
    textv2 = models.TextField(null=True)
    favorite = models.BooleanField(default=False)





class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True, blank=False)

    max_uses = models.FloatField(default=1, blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    used_by = models.ManyToManyField(User, through='PromoCodeUsage')
    expire_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.code


class PromoCodeUsage(models.Model):
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.promo_code.code





class Order(models.Model):
    transaction_id = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)
    idea = models.TextField(null=True, blank=True)



    complete = models.BooleanField(default=False)
    price = models.FloatField(null=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    type2 = models.CharField(max_length=100, null=True, blank=True)
    rawtext = models.TextField(null=True, blank=True)
    rawfile = models.FileField(upload_to='rawfiles/', null=True, blank=True)
    refund = models.BooleanField(default=False)
    result = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)
class UniqueText(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rawtext = models.TextField(null=True, blank=True)
    rawfile = models.FileField(upload_to='rawfiles/', null=True, blank=True)
    responsetext = models.TextField(null=True, blank=True)
    responsefile = models.FileField(upload_to='responsefiles/', null=True, blank=True)
    type = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)


    def __str__(self):
        return str(self.id)

class ExamText(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rawtext = models.TextField(null=True)

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    responsetext = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

@receiver(models.signals.post_delete, sender=UniqueText)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when  object is deleted.
    """
    # if instance.rawfile:
    #     if os.path.isfile(instance.rawfile.path):
    #         os.remove(instance.rawfile.path)
    if instance.responsefile:
        if os.path.isfile(instance.responsefile.path):
            os.remove(instance.responsefile.path)

@receiver(models.signals.post_delete, sender=Order)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
        Deletes file from filesystem
        when  object is deleted.
        """
    if instance.rawfile:
        if os.path.isfile(instance.rawfile.path):
            os.remove(instance.rawfile.path)




class Contact_us(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)



    message = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)



class VerificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

from django.db import models

class Crawl(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    result = models.TextField(blank=True, default='wait')

    status = models.CharField(max_length=100, blank=True)

