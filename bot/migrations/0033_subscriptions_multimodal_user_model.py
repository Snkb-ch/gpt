# Generated by Django 4.2 on 2023-10-06 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0032_remove_statistics_by_day_income_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptions',
            name='multimodal',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='model',
            field=models.CharField(default='gpt-3.5-turbo', max_length=50, null=True),
        ),
    ]
