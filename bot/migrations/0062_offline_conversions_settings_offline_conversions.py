# Generated by Django 4.2 on 2024-09-01 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0061_alter_user_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offline_conversions_settings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('target', models.CharField(max_length=50)),
                ('week_max', models.IntegerField(default=0)),
                ('week_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Offline_conversions',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('target', models.CharField(max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.user')),
            ],
        ),
    ]
