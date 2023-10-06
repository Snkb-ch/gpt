from datetime import datetime

import psycopg2 as pg

import os
import sys
from db import Database
from asgiref.sync import sync_to_async
from django.db.models import F
from django.forms import model_to_dict

# Получаем путь к текущему скрипту
script_path = os.path.abspath(__file__)
import openai_helper
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
from bot.models import User, Subscriptions,  Subscriptions_statistics, AnalyticsForDay, Statistics_by_day






class DBanalytics_for_sub_stat():

    @sync_to_async
    def exists(self, user_id):
        return Subscriptions_statistics.objects.filter(user_id=user_id).exists()

    @sync_to_async
    def new_sub_stats(self, user_id, sub_type, start_time = datetime.now()):
        Subscriptions_statistics.objects.create(
            user_id = user_id,
            sub_type = Subscriptions.objects.get(sub_id=sub_type),
            start_date = datetime.now()
        )


    @sync_to_async
    def set_inactive(self, user_id, expired_reason):

        if expired_reason == 'time':
            Subscriptions_statistics.objects.filter(user_id=user_id, active=True).update(active=False, end_date=User.objects.get(user_id=user_id).end_time, expired_reason=expired_reason)
        else:
            Subscriptions_statistics.objects.filter(user_id=user_id, active=True).update(active=False, end_date=datetime.now(),  expired_reason=expired_reason)


    @sync_to_async
    def role_edited(self, chat_id):
        sub_active = Subscriptions_statistics.objects.get(user_id=chat_id, active=True)
        sub_active.role_edited = F('role_edited') + 1
        sub_active.save()

    @sync_to_async
    def temp_edited(self, chat_id):
        sub_active = Subscriptions_statistics.objects.get(user_id=chat_id, active=True)
        sub_active.temp_edited = F('temp_edited') + 1
        sub_active.save()

    @sync_to_async
    def add_tokens(self, user_id, input_tokens, output_tokens):

        sub_active=Subscriptions_statistics.objects.get(user_id=user_id, active=True)
        sub_active.input_tokens += input_tokens
        sub_active.output_tokens += output_tokens


        sub_active.messages += 1
        sub_active.save()

    @sync_to_async
    def add_active_days(self, user_id):
        sub_active = Subscriptions_statistics.objects.get(user_id=user_id, active=True)
        sub_active.active_days = F('active_days') + 1
        sub_active.save()




class DBanalytics_for_day():




        @sync_to_async
        def add_sold(self, sub_id, price = 0):

            obj, created = AnalyticsForDay.objects.get_or_create(
                sub_type=Subscriptions.objects.get(sub_id=sub_id),
                day=datetime.now(),
                defaults={'sold': 1,
                'income': price}
            )

            if not created:
                obj.sold = F('sold') + 1
                obj.income = F('income') + price

                obj.save()

        @sync_to_async
        def add(self, sub_id, input_tokens, output_tokens, price):

            cost = price['input'] * input_tokens + price['output'] * output_tokens
            obj, created = AnalyticsForDay.objects.get_or_create(
                sub_type=Subscriptions.objects.get(sub_id=sub_id),
                day=datetime.now(),
                defaults={'input_tokens': input_tokens,
                          'output_tokens': output_tokens,
                            'messages': 1,
                            'costs': cost
                          }
            )

            if not created:
                obj.input_tokens = F('input_tokens') + input_tokens
                obj.output_tokens = F('output_tokens') + output_tokens
                obj.messages = F('messages') + 1
                obj.costs = F('costs') + cost

                obj.save()


        @sync_to_async
        def add_active_user(self, sub_id, new_user = False):
            obj, created = AnalyticsForDay.objects.get_or_create(
                sub_type=Subscriptions.objects.get(sub_id=sub_id),
                day=datetime.now(),
                defaults={'active_users': 1 ,
                'active_non_new_users': 0 if new_user else 1}
            )

            if not created:
                obj.active_users +=1
                if not new_user:
                    obj.active_non_new_users +=1

                obj.save()


class DBstatistics_by_day():


    @sync_to_async
    def add(self, user_id, input_tokens, output_tokens, price):
        day = datetime.now().date()
        cost = price['input'] * input_tokens + price['output'] * output_tokens
        obj, created = Statistics_by_day.objects.get_or_create(
            sub_stat=Subscriptions_statistics.objects.get(user_id=user_id, active=True),
            day=day,
            defaults={'input_tokens': input_tokens,
                      'output_tokens': output_tokens,
                      'messages': 1,
                      'costs': cost
                      }
        )

        if not created:
            obj.input_tokens += input_tokens
            obj.output_tokens += output_tokens
            obj.messages += 1
            obj.costs += cost

            obj.save()
