# Generated by Django 4.2 on 2023-04-24 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basegpt', '0002_remove_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crawl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('result', models.TextField(blank=True, default='wait')),
                ('status', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
