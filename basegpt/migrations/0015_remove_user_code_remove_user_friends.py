# Generated by Django 4.1.7 on 2023-03-17 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basegpt', '0014_rename_promo_code_personal_user_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='code',
        ),
        migrations.RemoveField(
            model_name='user',
            name='friends',
        ),
    ]
