# Generated by Django 4.1.7 on 2023-03-13 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basegpt', '0002_remove_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
