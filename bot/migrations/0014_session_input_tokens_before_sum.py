# Generated by Django 4.2 on 2023-09-22 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0013_session_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='input_tokens_before_sum',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
