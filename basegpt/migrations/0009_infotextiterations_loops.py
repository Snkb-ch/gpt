# Generated by Django 4.2 on 2024-04-30 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basegpt', '0008_remove_result_textv1_remove_result_textv2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='infotextiterations',
            name='loops',
            field=models.IntegerField(null=True),
        ),
    ]
