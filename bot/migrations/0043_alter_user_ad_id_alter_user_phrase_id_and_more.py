# Generated by Django 4.2 on 2023-10-09 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0042_alter_user_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='ad_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phrase_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='utm_campaign',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
