# Generated by Django 4.2 on 2023-09-29 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0024_user_blocked'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalyticsForDay',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('day', models.DateField()),
                ('active_users', models.IntegerField(default=0)),
                ('sold', models.IntegerField(default=0)),
                ('input_tokens', models.BigIntegerField(default=0)),
                ('output_tokens', models.BigIntegerField(default=0)),
                ('messages', models.IntegerField(default=0)),
                ('sub_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.subscriptions')),
            ],
        ),
        migrations.AddConstraint(
            model_name='analyticsforday',
            constraint=models.UniqueConstraint(fields=('sub_type', 'day'), name='analytics_for_day_sub_type_day_key'),
        ),
    ]
