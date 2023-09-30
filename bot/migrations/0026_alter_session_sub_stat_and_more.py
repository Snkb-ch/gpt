# Generated by Django 4.2 on 2023-09-30 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0025_analyticsforday_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='sub_stat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.subscriptions_statistics'),
        ),
        migrations.AlterField(
            model_name='subscriptions_statistics',
            name='sub_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.subscriptions'),
        ),
        migrations.AlterField(
            model_name='subscriptions_statistics',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.user'),
        ),
    ]
