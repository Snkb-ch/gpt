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
    def get_sub_name_from_user_mode(self, user_id):
        model =  User.objects.get(user_id=user_id).model

        if model == 'gpt-4':
            return 'gpt-4o'
        elif model == 'gpt-3.5':
            return 'gpt-4o-mini'
        elif model == 'llama-3-70':
            return 'Llama-3'
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
            return 'gpt-4o', multi_k
        elif model == 'gpt-3.5':
            return 'gpt-4o-mini', multi_k

        elif model == 'llama-3-70':
            return 'meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo',  multi_k
        elif model == 'llama-3-400':
            return 'meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo',  multi_k


    # @sync_to_async
    # def get_sub_models(self, sub_id):
    #     models_names_list = Subscriptions_models.objects.filter(sub_id=sub_id).values_
    #     return list(models_list)

    @sync_to_async
    def set_next_model(self, sub_id, user_id):
        user_model = User.objects.get(user_id=user_id).model



        models_list = Subscriptions_models.objects.filter(sub_id=sub_id).values_list('model', flat=True)
        models_list = list(models_list)


        models_list = Models.objects.filter(id__in=models_list).values_list('model_name_user', flat=True)
        models_list = list(models_list)


        if user_model in models_list:
            index = models_list.index(user_model)
            if index == len(models_list) - 1:
                model = models_list[0]
            else:
                model = models_list[index + 1]
        else:
            model = models_list[0]
        User.objects.filter(user_id=user_id).update(model=model)

        return model




    @sync_to_async
    def get_model_config(self, user_id):




        sub_name = User.objects.get(user_id=user_id).sub_type.sub_name
        user_sub_id = User.objects.get(user_id=user_id).sub_type.sub_id
        model = User.objects.get(user_id=user_id).model

        if sub_name == 'free':

            return None



        models_in_sub = Subscriptions_models.objects.filter(sub_id=user_sub_id).values_list('model', flat=True)
        models_in_sub = list(models_in_sub)
        models_in_sub_names = Models.objects.filter(id__in=models_in_sub).values_list('model_name_user', flat=True)
        models_in_sub_names = list(models_in_sub_names)

        # model that in models_in_sub_names

        if model in models_in_sub_names:
            model_name = model

        else:
            model_name = models_in_sub_names[0]
            User.objects.filter(user_id=user_id).update(model=model_name)
        # fins model  that model id in models_in_sub and in models_in_sub_names
        model = Models.objects.get(model_name_user=model_name, id__in=models_in_sub)



        custom_temp = User.objects.get(user_id=user_id).custom_temp
        conf = {
            'model': model.model_name,
            'max_tokens': model.max_tokens,
            'multi_k': model.model_k,
            'custom_temp': custom_temp,


        }

        return conf
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
    def get_act_users(self):
        # list of users_id with sub_name != 'free' and 'trial'
        sub_id = Subscriptions.objects.filter(~Q(sub_name='free') & ~Q(sub_name='trial')).values_list('sub_id', flat=True)
        list = []
        for i in sub_id:
            list.append(User.objects.filter(sub_type=i, blocked = False).values_list('user_id', flat=True   ))

        list = [item for sublist in list for item in sublist]
        return list



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
    def  set_utm(self, user_id, utm_campaign = None, group_id= None, client_id_metrika= None):

        user = User.objects.get(user_id=user_id)

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


    @sync_to_async
    def add_offline_conversions(self, user_id, target):
        if not Offline_conversions.objects.filter(user_id=user_id, target=target).exists():
            Offline_conversions.objects.create(user_id=user_id, target=target)
        
    @sync_to_async
    def add_offline_conversions_settings_count(self, target):
        import random

        obj, created = Offline_conversions_settings.objects.get_or_create(target=target, day_count=1)

        if not created:
            obj.day_count += 1
            if obj.day_count >= obj.day_max:
                obj.day_count = 0
                obj.day_last_reset = datetime.now()
                obj.day_max = random.randint(1,3)


            

            obj.save()

    @sync_to_async
    def  check_offline_conversions_settings_count(self, target):
        obj = Offline_conversions_settings.objects.get(target=target)
        if obj.day_count < obj.day_max and obj.day_last_reset < datetime.now().date():
            return True
        else:
            return False

    @sync_to_async
    def get_offline_conversions_of_user(self, user_id, target):
        if Offline_conversions.objects.filter(user_id=user_id, target=target).exists():
            return True
        else:
            return False








        
    











