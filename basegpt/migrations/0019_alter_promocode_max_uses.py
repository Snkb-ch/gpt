# Generated by Django 4.1.7 on 2023-03-17 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basegpt', '0018_alter_promocode_expire_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocode',
            name='max_uses',
            field=models.FloatField(blank=True, default=1, null=True),
        ),
    ]
