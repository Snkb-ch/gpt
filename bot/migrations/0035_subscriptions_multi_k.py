# Generated by Django 4.2 on 2023-10-06 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0034_rename_multimodal_subscriptions_multimodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptions',
            name='multi_k',
            field=models.IntegerField(null=True),
        ),
    ]
