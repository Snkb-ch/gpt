# Generated by Django 4.1.7 on 2023-03-17 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basegpt', '0015_remove_user_code_remove_user_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='code',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.IntegerField(default=0),
        ),
    ]
