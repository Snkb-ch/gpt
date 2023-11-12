# Generated by Django 4.2 on 2023-11-12 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0047_subscriptions_gen_im'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='phrase_id',
            new_name='client_id',
        ),
        migrations.AddField(
            model_name='user',
            name='group_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
