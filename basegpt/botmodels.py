

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


from bot.models import User


def is_active_by_email(email):
    user = User.objects.get(email=email)
    return user.status

print (is_active_by_email('snk2032@gmail.com'))




