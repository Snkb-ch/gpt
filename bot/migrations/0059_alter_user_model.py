# Generated by Django 4.2 on 2024-08-07 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0058_alter_user_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='model',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
