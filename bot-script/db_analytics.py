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
from bot.models import User, Subscriptions, Period, AnalyticsForMonth, AnalyticsPeriods, Session, Subscriptions_statistics


class DBanalytics_for_month:


    def begin_date(self):
        now = datetime.now()
        return now.strftime("%Y-%m-01")



    @sync_to_async
    def add_input_tokens(self, sub_id, input_tokens):
        obj, created =AnalyticsForMonth.objects.get_or_create(
            sub_type=Subscriptions.objects.get(sub_id=sub_id),
            begin_date=self.begin_date(),
            defaults={'input_tokens': input_tokens}
        )

        if not created:
            obj.input_tokens = F('input_tokens') + input_tokens
            obj.save()

    @sync_to_async
    def get_input_tokens(self, sub_id):
        return AnalyticsForMonth.objects.get(sub_type=sub_id, begin_date=self.begin_date()).input_tokens
    @sync_to_async
    def add_output_tokens(self, sub_id, output_tokens):
        obj, created = AnalyticsForMonth.objects.get_or_create(
            sub_type=Subscriptions.objects.get(sub_id=sub_id),
            begin_date=self.begin_date(),
            defaults={'output_tokens': output_tokens}
        )

        if not created:
            obj.output_tokens = F('output_tokens') + output_tokens
            obj.save()
    @sync_to_async
    def get_output_tokens(self, sub_id):
        return AnalyticsForMonth.objects.get(sub_type=sub_id, begin_date=self.begin_date()).output_tokens


    @sync_to_async
    def add_expired_time(self, sub_id):
        obj, created = AnalyticsForMonth.objects.get_or_create(
            sub_type=Subscriptions.objects.get(sub_id=sub_id),
            begin_date=self.begin_date(),
            defaults={'expired_time': 1}
        )

        if not created:
            obj.expired_time = F('expired_time') + 1
            obj.save()
    @sync_to_async
    def get_expired_time(self, sub_id):
        return AnalyticsForMonth.objects.get(sub_type=sub_id, begin_date=self.begin_date()).expired_time
    @sync_to_async
    def add_expired_tokens(self, sub_id):
        obj, created = AnalyticsForMonth.objects.get_or_create(
            sub_type=Subscriptions.objects.get(sub_id=sub_id),
            begin_date=self.begin_date(),
            defaults={'expired_tokens': 1}
        )

        if not created:
            obj.expired_tokens = F('expired_tokens') + 1
            obj.save()
    @sync_to_async
    def add_sold(self, sub_id):
        AnalyticsForMonth.objects.update_or_create(
            sub_type=Subscriptions.objects.get(sub_id=sub_id),
            begin_date=self.begin_date(),
            defaults={'sold': F('sold') + 1}
        )

    @sync_to_async
    def get_sold(self, sub_id):
        return AnalyticsForMonth.objects.get(sub_type=sub_id, begin_date=self.begin_date()).sold


    @sync_to_async
    def add_expired(self, sub_id):
        obj, created = AnalyticsForMonth.objects.get_or_create(
            sub_type=Subscriptions.objects.get(sub_id=sub_id),
            begin_date=self.begin_date(),
            defaults={'expired': 1}
        )
        if not created:
            obj.expired = F('expired') + 1
            obj.save()

    @sync_to_async
    def get_expired(self, sub_id):
        return AnalyticsForMonth.objects.get(sub_type=sub_id, begin_date=self.begin_date()).expired
    @sync_to_async
    def add_income(self, sub_id, income):
        obj, created = AnalyticsForMonth.objects.get_or_create(
            sub_type=Subscriptions.objects.get(sub_id=sub_id),
            begin_date=self.begin_date(),
            defaults={'income': income}
        )

        if not created:
            obj.income = F('income') + income
            obj.save()


    @sync_to_async
    def get_income(self, sub_id):
        return AnalyticsForMonth.objects.get(sub_type=Subscriptions.objects.get(sub_id=sub_id), begin_date=self.begin_date()).income
    @sync_to_async
    def add_temp_edited(self, sub_id):
        obj, created = AnalyticsForMonth.objects.get_or_create(
            sub_type=Subscriptions.objects.get(sub_id=sub_id),
            begin_date=self.begin_date(),
            defaults={'temp_edited': 1}
        )
        if not created:
            obj.temp_edited = F('temp_edited') + 1
            obj.save()

    @sync_to_async
    def get_temp_edited(self, sub_id):
        return AnalyticsForMonth.objects.get(sub_type=sub_id, begin_date=self.begin_date()).temp_edited
    @sync_to_async
    def add_role_edited(self, sub_id):
        obj, created = AnalyticsForMonth.objects.get_or_create(
            sub_type=Subscriptions.objects.get(sub_id=sub_id),
            begin_date=self.begin_date(),
            defaults={'role_edited': 1}
        )
        if not created:
            obj.role_edited = F('role_edited') + 1
            obj.save()
    @sync_to_async
    def get_role_edited(self, sub_id):
        return AnalyticsForMonth.objects.get(sub_type=sub_id, begin_date=self.begin_date()).role_edited

class DBanalytics_for_periods:

    def day(self):
        date = datetime.now()
        date_string = date.strftime("%Y-%m-%d")
        date_obj = datetime.strptime(date_string, "%Y-%m-%d")

        # Get the day type (e.g., Monday, Tuesday, etc.) using the strftime method
        day_type = date_obj.strftime("%A")

        return day_type

    def date(self):
        now = datetime.now().replace(day=1)
        return now.strftime("%Y-%m-%d")


    def get_period_id(self, time):
         # Replace this with the desired time

        return Period.objects.filter(begin__lt=time, end__gte=time).first().id_period


    @sync_to_async
    def add(self, sub_type, tokens):
        print(self.date())
        print(self.day())
        print(self.get_period_id(datetime.now().time()))




        obj, created = AnalyticsPeriods.objects.get_or_create(
            sub_type=Subscriptions.objects.get(sub_id=sub_type),
            month=self.date(),
            day=self.day(),
            period=self.get_period_id(datetime.now().time()),
            defaults={'tokens': tokens, 'users': 1}
        )

        if not created:
            obj.tokens = F('tokens') + tokens
            obj.users = F('users') + 1
            obj.save()

class DBanalytics_for_sessions:

    @sync_to_async
    def new_sub_stats(self, user_id, sub_type):
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
    def add_session(self,user_id,  sub_type, start_time):

        Session.objects.create(
            sub_stat = Subscriptions_statistics.objects.get(user_id=user_id, active=True),

            start_time = start_time)



    @sync_to_async
    def close_session(self, user_id, end_time):
        if Subscriptions_statistics.objects.filter(user_id=user_id, active=True).exists():
            sub_stat = Subscriptions_statistics.objects.get(user_id=user_id, active=True)
            Session.objects.filter(sub_stat=sub_stat, closed=False).update(closed=True, end_time=end_time)





    @sync_to_async
    def update_session_input(self, chat_id, input_tokens, input_tokens_before_sum):
        active_session = Session.objects.get(sub_stat=Subscriptions_statistics.objects.get(user_id=chat_id, active=True), closed=False)
        active_session.input_tokens = F('input_tokens') + input_tokens
        active_session.input_tokens_before_sum = F('input_tokens') + input_tokens_before_sum

        active_session.messages = F('messages') + 1




        active_session.save()





    @sync_to_async
    def update_session_output(self, chat_id, output_tokens):
        active_session = Session.objects.get(sub_stat=Subscriptions_statistics.objects.get(user_id=chat_id, active=True), closed=False)
        active_session.output_tokens = F('output_tokens') + output_tokens

        active_session.save()


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

















