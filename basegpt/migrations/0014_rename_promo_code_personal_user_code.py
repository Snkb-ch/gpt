# Generated by Django 4.1.7 on 2023-03-17 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basegpt', '0013_user_friends_alter_user_promo_code_personal'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='promo_code_personal',
            new_name='code',
        ),
    ]
