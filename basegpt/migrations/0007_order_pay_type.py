# Generated by Django 4.2 on 2024-04-13 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basegpt', '0006_result_raw_all_count_result_raw_procent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='pay_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]