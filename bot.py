import os

import os
import django

import os
import sys
import django



# Указываем правильный путь к файлу settings.py относительно папки gpt
os.environ["DJANGO_SETTINGS_MODULE"] = "gpt.settings"
django.setup()

# Остальная часть вашего скрипта

from bot.models import *
class Get:

    def get(self):
        print(User.objects.all().using('bottg'))


o = Get()
o.get()