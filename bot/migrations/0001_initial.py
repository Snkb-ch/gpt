# Generated by Django 4.2 on 2023-08-16 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnalyticsForMonth',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('begin_date', models.DateField()),
                ('active', models.IntegerField(default=1)),
                ('input_tokens', models.BigIntegerField(default=0)),
                ('output_tokens', models.BigIntegerField(default=0)),
                ('total_tokens', models.BigIntegerField(default=0)),
                ('expired_time', models.IntegerField(default=0)),
                ('expired_tokens', models.IntegerField(default=0)),
                ('sold', models.IntegerField(default=0)),
                ('expired', models.IntegerField(default=0)),
                ('income', models.IntegerField(default=0)),
                ('temp_edited', models.IntegerField(default=0)),
                ('role_edited', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='AnalyticsPeriods',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('month', models.DateField()),
                ('day', models.CharField(max_length=20)),
                ('period', models.IntegerField()),
                ('tokens', models.IntegerField()),
                ('users', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id_period', models.AutoField(primary_key=True, serialize=False)),
                ('begin', models.TimeField(null=True)),
                ('end', models.TimeField(null=True)),
            ],
            options={
                'managed': 'bottg',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('sub_id', models.AutoField(primary_key=True, serialize=False)),
                ('sub_name', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('max_tokens', models.IntegerField(null=True)),
                ('price', models.IntegerField(null=True)),
                ('edit_temp', models.BooleanField(default=False)),
                ('edit_role', models.BooleanField(default=False)),
                ('duration', models.IntegerField(null=True)),
                ('temp', models.IntegerField(default=1)),
                ('for_sale', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(default='active', max_length=25)),
                ('used_tokens', models.IntegerField(default=0)),
                ('time_sub', models.DateField(auto_now_add=True)),
                ('end_time', models.DateField(null=True)),
                ('custom_temp', models.IntegerField(default=1)),
                ('email', models.CharField(max_length=50, null=True)),
                ('expired_date', models.DateField(null=True)),
                ('admin', models.BooleanField(default=False)),
                ('sub_type', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='bot.subscription')),
            ],
        ),
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.UniqueConstraint(fields=('sub_id',), name='subscriptions_pkey'),
        ),
        migrations.AddConstraint(
            model_name='period',
            constraint=models.UniqueConstraint(fields=('id_period',), name='periods_pkey'),
        ),
        migrations.AddField(
            model_name='analyticsperiods',
            name='sub_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.subscription'),
        ),
        migrations.AddField(
            model_name='analyticsformonth',
            name='sub_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.subscription'),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(fields=('user_id',), name='users_user_id_key'),
        ),
        migrations.AddConstraint(
            model_name='analyticsperiods',
            constraint=models.UniqueConstraint(fields=('sub_type', 'day', 'month', 'period'), name='analytics_periods_sub_type_day_month_period_key'),
        ),
        migrations.AddConstraint(
            model_name='analyticsformonth',
            constraint=models.UniqueConstraint(fields=('sub_type', 'begin_date'), name='analytics_for_month_sub_type_beginning_key'),
        ),
    ]
