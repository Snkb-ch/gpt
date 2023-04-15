# Generated by Django 4.1.7 on 2023-03-17 17:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('basegpt', '0011_user_promo_code_personal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='promo_code_personal',
            field=models.CharField(default=uuid.uuid4, max_length=50, unique=True),
        ),
    ]
