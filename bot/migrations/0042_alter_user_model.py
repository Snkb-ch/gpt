# Generated by Django 4.2 on 2023-10-09 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0041_remove_user_region_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='model',
            field=models.CharField(default='gpt-4', max_length=50, null=True),
        ),
    ]