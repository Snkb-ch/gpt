# Generated by Django 4.2 on 2023-10-04 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0026_alter_session_sub_stat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='analyticsforday',
            name='active_non_new_users',
            field=models.IntegerField(default=0),
        ),
    ]