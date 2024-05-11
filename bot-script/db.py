from datetime import datetime, timedelta

import psycopg2 as pg

import os
import sys
from django.db.models import Q
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
import django
from django.conf import settings
# Установите переменную окружения DJANGO_SETTINGS_MODULE для указания файла настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gpt.settings")
configured_apps = list(settings.INSTALLED_APPS)

# Убираем 'adrf' из списка
if 'adrf' in configured_apps:
    configured_apps.remove('adrf')

# Переопределяем INSTALLED_APPS в settings
settings.INSTALLED_APPS = tuple(configured_apps)


# Теперь выполните настройку Django
django.setup()
from bot.models import *




class Database:

    @sync_to_async
    def add_user(self, user_id):

        #trial sub
        sub_id = Subscriptions.objects.get(sub_name='trial', for_sale=True).sub_id

        User.objects.create(user_id=user_id, sub_type=Subscriptions.objects.get(sub_id=sub_id))

    @sync_to_async
    def get_user_model(self, user_id):
        return User.objects.get(user_id=user_id).model
    @sync_to_async
    def set_user_model(self, user_id, model):
        User.objects.filter(user_id=user_id).update(model=model)
    @sync_to_async
    def get_sub_multimodel(self, sub_id):

        return Subscriptions.objects.get(sub_id=sub_id).multimodel

    @sync_to_async
    def get_sub_multi_k(self, sub_id):
        return Subscriptions.objects.get(sub_id=sub_id).multi_k

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
    def get_sub_info(self, sub_id):
        #return dict
        values = Subscriptions.objects.filter(sub_id=sub_id).values('sub_name', 'price', 'cost').first()

        return values



    @sync_to_async
    def get_max_tokens(self, user_id):
        return User.objects.get(user_id=user_id).sub_type.max_tokens
    @sync_to_async
    def get_used_tokens(self, user_id):
        return User.objects.get(user_id=user_id).used_tokens
    @sync_to_async
    def get_gen_im(self, sub_type):
        return Subscriptions.objects.get(sub_id=sub_type).gen_im

    @sync_to_async
    def set_used_tokens(self, user_id, tokens):
        user = User.objects.get(user_id=user_id)
        user.used_tokens = tokens
        user.save()

    @sync_to_async
    def get_active_days(self, user_id):
        return User.objects.get(user_id=user_id).active_days

    @sync_to_async
    def update_used_tokens(self, user_id, tokens):
        user = User.objects.get(user_id=user_id)
        user.used_tokens += tokens
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


    def get_model_name(self, model, multi_k):
        if model == 'gpt-4':
            return 'gpt-4-turbo-2024-04-09', multi_k
        elif model == 'gpt-3.5':
            return 'gpt-3.5-turbo', multi_k
        elif model == 'llama-3-70':
            return 'meta-llama/Llama-3-70b-chat-hf', multi_k // 2

    @sync_to_async
    def get_model_config(self, user_id):





        multimodel_3 = False
        multimodel = Subscriptions.objects.get(sub_id=User.objects.get(user_id=user_id).sub_type.sub_id).multimodel
        multi_k = Subscriptions.objects.get(sub_id=User.objects.get(user_id=user_id).sub_type.sub_id).multi_k
        model = User.objects.get(user_id=user_id).model
        if multimodel:

            if model == 'gpt-3.5' or model == 'llama-3-70':
                multimodel_3 = True



        custom_temp = User.objects.get(user_id=user_id).custom_temp

        model,  multi_k = self.get_model_name(model, multi_k)
        sub_name = User.objects.get(user_id=user_id).sub_type.sub_name
        if sub_name == 'trial':
            model = 'gpt-3.5'
        data_dict = {'model': model, 'custom_temp': custom_temp, 'multimodel_3': multimodel_3, 'multi_k': multi_k}
        print(data_dict)
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
    def reset_email(self, user_id):
        user = User.objects.get(user_id=user_id)
        user.email = None
        user.save()

    @sync_to_async
    def get_all_users(self):
        # list of users_id

        return list(User.objects.filter(blocked = False).values_list('user_id', flat=True))

    @sync_to_async
    def get_sub_ending_users(self):
        date = datetime.now()



        users = User.objects.filter( status='active', end_time=date + timedelta(days= 1), blocked = False).values_list('user_id', flat=True)





        return list(users)
    @sync_to_async
    def get_all_inactive_users(self):
        date = datetime.now()



        users = list(User.objects.filter(status='inactive', reminder_date=date, blocked = False).values_list('user_id', flat=True))

        # # set reminder_date for users
        User.objects.filter(status='inactive', reminder_date=date).update(reminder_date=date + timedelta(days=30))
        return users

    @sync_to_async
    def set_inactive(self, user_id):
        date = datetime.now()
        User.objects.filter(user_id=user_id).update(status='inactive', reminder_date=date + timedelta(days=14), sub_type = Subscriptions.objects.get(sub_name='free'))

    @sync_to_async
    def set_inactive_auto(self):
        date = datetime.now()
        users = User.objects.filter(status='active', end_time=date).values_list('user_id', flat=True)
        user_list = list(users)
        users.update(status='inactive', reminder_date=date + timedelta(days=14), sub_type = Subscriptions.objects.get(sub_name='free'))
        return user_list



    @sync_to_async
    def is_admin(self, user_id):
        return User.objects.get(user_id=user_id).admin

    @sync_to_async
    def get_subs_for_sale(self):
        # по возрастанию цены
        subs_dict = Subscriptions.objects.filter(for_sale=True).exclude(sub_name='trial').order_by('price').values('sub_id', 'sub_name', 'price')


        return list(subs_dict)

    @sync_to_async
    def get_last_message(self, user_id):
        return User.objects.get(user_id=user_id).last_message

    @sync_to_async
    def set_last_message(self, user_id, date):
        user = User.objects.get(user_id=user_id)
        user.last_message = date
        user.save()


    @sync_to_async
    def set_blocked_user(self, user_id):
        user = User.objects.get(user_id=user_id)
        user.blocked = True
        user.save()

    @sync_to_async
    def get_users_for_reset_history(self):
        date = datetime.now()
        return list(User.objects.filter(status='active', last_message__lt=date - timedelta(days=2)).values_list('user_id', flat=True))

    @sync_to_async
    def get_active_trial_users(self):
        date = datetime.now()

        sub_trial_id = Subscriptions.objects.filter(sub_name='trial').values_list('sub_id', flat=True)
        list = []
        for i in sub_trial_id:
            list.append(User.objects.filter(sub_type=i, status='active', blocked = False, last_message = date - timedelta(days=1)).values_list('user_id', flat=True))

        list = [item for sublist in list for item in sublist]


        return list

    @sync_to_async
    def get_trial_users(self):
        date = datetime.now()

        sub_trial_id = Subscriptions.objects.filter(sub_name='trial').values_list('sub_id', flat=True)
        list = []
        for i in sub_trial_id:
            list.append(User.objects.filter(sub_type=i, status='active').values_list('user_id', flat=True))

        list = [item for sublist in list for item in sublist]
        return list

    @sync_to_async
    def get_model(self, user_id):
        return Subscriptions.objects.get(sub_id=User.objects.get(user_id=user_id).sub_type.sub_id).model




    @sync_to_async
    def update_user(self, user_id, sub_id):
        user = User.objects.get(user_id=user_id)
        user.sub_type = Subscriptions.objects.get(sub_id=sub_id)
        user.status = 'active'
        user.used_tokens = 0
        user.custom_temp = 1
        user.last_message = None

        user.time_sub = datetime.now()
        user.end_time = datetime.now() + timedelta(days=Subscriptions.objects.get(sub_id=sub_id).duration)

        user.save()

    @sync_to_async
    def get_custom_users(self, status, sub_name, end_date, time_sub):
        return list(User.objects.filter(status=status, sub_type=Subscriptions.objects.get(sub_name=sub_name), end_time=end_date, time_sub=time_sub).values_list('user_id', flat=True))


    @sync_to_async
    def get_admin_users(self):
        return list(User.objects.filter(admin=True, blocked = False).values_list('user_id', flat=True))\

    @sync_to_async
    def get_client_id(self, user_id):
        return User.objects.get(user_id=user_id).client_id_metrika

    @sync_to_async
    def client_id_exist(self, user_id):
        return User.objects.get(user_id=user_id).client_id_metrika
    @sync_to_async
    def count_new_users_trial(self):
        date = datetime.now()
        trial_id = Subscriptions.objects.filter(sub_name='trial').values_list('sub_id', flat=True)
        k = 0
        for i in trial_id:
            k += User.objects.filter(time_sub=date, sub_type=i).count()
        return k

    @sync_to_async
    def count_new_users_not_trial(self):

        not_trial_or_free = User.objects.filter(~Q(sub_type__sub_name='free') & ~Q(sub_type__sub_name='trial'), time_sub=datetime.now()).count()

        return not_trial_or_free

    @sync_to_async
    def set_unblocked_user(self, user_id):

        User.objects.filter(user_id=user_id).update(blocked=False)



    @sync_to_async
    def  set_utm(self, user_id, utm_source, utm_campaign = None, group_id= None, client_id_metrika= None):

        user = User.objects.get(user_id=user_id)
        user.utm_source = utm_source if utm_source and utm_source!= 'None' else None
        user.utm_campaign = utm_campaign if utm_campaign and utm_campaign!= 'None' else None

        user.group_id = group_id if group_id and group_id!= 'None' else None


        user.client_id_metrika = client_id_metrika if client_id_metrika and client_id_metrika != 'None' else None
        user.save()

    @sync_to_async
    def get_promo_used(self, user_id):
        return User.objects.get(user_id=user_id).tg_channel_used


    @sync_to_async
    def add_promo_used(self, user_id):
        user = User.objects.get(user_id=user_id)
        user.tg_channel_used += 1
        user.save()

    @sync_to_async
    def add_poll_answer(self, user_id, answer):
        user = User.objects.get(user_id=user_id)
        user.poll_answers = answer
        user.save()