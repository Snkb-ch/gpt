# Generated by Django 4.2 on 2023-10-07 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0037_remove_user_region_name_remove_user_utm_term_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='campaign_type',
        ),
    ]
