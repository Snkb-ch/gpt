# Generated by Django 4.2 on 2023-09-22 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0018_alter_subscriptions_statistics_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptions_statistics',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
