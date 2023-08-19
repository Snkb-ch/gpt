# Generated by Django 4.2 on 2023-08-17 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_alter_user_used_tokens'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='admin',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='custom_temp',
            field=models.FloatField(default=1, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='sub_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='bot.subscription'),
        ),
        migrations.AlterField(
            model_name='user',
            name='time_sub',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
