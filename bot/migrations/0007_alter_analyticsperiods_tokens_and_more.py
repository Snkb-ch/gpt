# Generated by Django 4.2 on 2023-08-17 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0006_rename_subscription_subscriptions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analyticsperiods',
            name='tokens',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='subscriptions',
            name='temp',
            field=models.FloatField(default=1, null=True),
        ),
    ]
