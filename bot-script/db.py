from datetime import datetime, timedelta

import psycopg2 as pg

import os
import sys

from asgiref.sync import sync_to_async
from django.forms import model_to_dict

# Получаем путь к текущему скрипту
script_path = os.path.abspath(__file__)

# Получаем путь к директории, содержащей текущий скрипт
script_dir = os.path.dirname(script_path)

# Получаем путь к корневой директории проекта (по одному уровню выше)
project_root = os.path.dirname(script_dir)

# Добавляем путь к корневой директории в переменную окружения PYTHONPATH
sys.path.insert(0, project_root)

# Теперь можно импортировать модели из bot.models

# Установите переменную окружения DJANGO_SETTINGS_MODULE для указания файла настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gpt.settings")

# Импортируем и настраиваем Django настройки
import django
django.setup()
from bot.models import User, Subscriptions, Period, AnalyticsForMonth, AnalyticsPeriods




class Database:

    @sync_to_async
    def add_user(self, user_id):
        # use django oRM
        User.objects.create(user_id=user_id, sub_type=Subscriptions.objects.get(sub_id=1))

    @sync_to_async
    def user_exists(self, user_id):

            return User.objects.filter(user_id=user_id).exists()
    @sync_to_async
    def get_status(self, user_id):
        return User.objects.get(user_id=user_id).status
    @sync_to_async
    def set_status(self, user_id, status):
        user = User.objects.get(user_id=user_id)
        user.status = status
        user.save()
    @sync_to_async
    def get_sub_type(self, user_id):

        return  User.objects.get(user_id=user_id).sub_type.sub_id
    @sync_to_async
    def set_sub_type(self, user_id, sub_type):
        user = User.objects.get(user_id=user_id)
        user.sub_type = Subscriptions.objects.get(sub_id=sub_type)
        user.save()
    @sync_to_async
    def get_sub_name_from_user(self, user_id):
        return User.objects.get(user_id=user_id).sub_type.sub_name
    @sync_to_async
    def get_sub_name(self, sub_id):
        return Subscriptions.objects.get(sub_id=sub_id).sub_name

    @sync_to_async
    def get_max_tokens(self, user_id):
        return User.objects.get(user_id=user_id).sub_type.max_tokens
    @sync_to_async
    def get_used_tokens(self, user_id):
        return User.objects.get(user_id=user_id).used_tokens

    @sync_to_async
    def set_used_tokens(self, user_id, tokens):
        user = User.objects.get(user_id=user_id)
        user.used_tokens = tokens
        user.save()
    @sync_to_async
    def get_duration_sub(self, user_id):
        return User.objects.get(user_id=user_id).sub_type.duration
    @sync_to_async
    def set_time_sub(self, user_id, date):
        user = User.objects.get(user_id=user_id)
        user.time_sub = date
        user.save()
    @sync_to_async
    def get_time_sub(self, user_id):
        return User.objects.get(user_id=user_id).time_sub
    @sync_to_async
    def set_end_time(self, user_id, end_date):
        user = User.objects.get(user_id=user_id)
        user.end_time = end_date
        user.save()
    @sync_to_async
    def get_end_time(self, user_id):
        return User.objects.get(user_id=user_id).end_time
    @sync_to_async
    def get_user_params(self, user_id):
        user_instance = User.objects.get(user_id=user_id)

        # Convert the user instance to a dictionary
        data_dict = model_to_dict(user_instance)

        return data_dict
    @sync_to_async
    def get_model_config(self, user_id):
        model = Subscriptions.objects.get(sub_id=User.objects.get(user_id=user_id).sub_type.sub_id).model
        custom_temp = User.objects.get(user_id=user_id).custom_temp
        data_dict = {'model': model, 'custom_temp': custom_temp}
        return data_dict
    @sync_to_async
    def get_price(self, sub_id):
        return Subscriptions.objects.get(sub_id=sub_id).price
    @sync_to_async
    def set_custom_temp(self, user_id, temp):
        user = User.objects.get(user_id=user_id)
        user.custom_temp = temp
        user.save()
    @sync_to_async
    def get_edit_role(self, user_id):
        return Subscriptions.objects.get(sub_id=User.objects.get(user_id=user_id).sub_type.sub_id).edit_role
    @sync_to_async
    def get_edit_temp(self, user_id):
        return Subscriptions.objects.get(sub_id=User.objects.get(user_id=user_id).sub_type.sub_id).edit_temp
    @sync_to_async
    def get_email(self, user_id):
        return User.objects.get(user_id=user_id).email
    @sync_to_async
    def set_email(self, user_id, email):
        user = User.objects.get(user_id=user_id)
        user.email = email
        user.save()

    @sync_to_async
    def get_all_users(self):
        # list of users_id

        return list(User.objects.all().values_list('user_id', flat=True))

    @sync_to_async
    def get_all_inactive_users(self):
        date = datetime.now()




        # # set expired_date for users
        User.objects.filter(status='inactive', expired_date=date).update(expired_date=date + timedelta(days=30))
        return list(User.objects.filter(status='inactive', expired_date=date).values_list('user_id', flat=True))

    @sync_to_async
    def set_inactive(self, user_id):
        date = datetime.now()
        User.objects.filter(user_id=user_id).update(status='inactive', expired_date=date + timedelta(days=14))
    @sync_to_async
    def is_admin(self, user_id):
        return User.objects.get(user_id=user_id).admin

    @sync_to_async
    def get_subs_for_sale(self):
        subs_dict = Subscriptions.objects.filter(for_sale=True).values('sub_id', 'sub_name', 'price')

        return list(subs_dict)

#
db = Database()



