# Generated by Django 4.2 on 2024-08-10 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('balance', models.FloatField(default=0)),
                ('email_verified', models.BooleanField(default=False)),
                ('code', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('friends', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Crawl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('result', models.TextField(blank=True, default='wait')),
                ('status', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('idea', models.TextField(blank=True, null=True)),
                ('complete', models.BooleanField(default=False)),
                ('price', models.FloatField(null=True)),
                ('type', models.CharField(blank=True, max_length=100, null=True)),
                ('type2', models.CharField(blank=True, max_length=100, null=True)),
                ('rawtext', models.TextField(blank=True, null=True)),
                ('rawfile', models.FileField(blank=True, null=True, upload_to='rawfiles/')),
                ('refund', models.BooleanField(default=False)),
                ('result', models.BooleanField(default=False)),
                ('pay_type', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('max_uses', models.FloatField(blank=True, default=1, null=True)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('expire_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VerificationToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UniqueText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rawtext', models.TextField(blank=True, null=True)),
                ('rawfile', models.FileField(blank=True, null=True, upload_to='rawfiles/')),
                ('responsetext', models.TextField(blank=True, null=True)),
                ('responsefile', models.FileField(blank=True, null=True, upload_to='responsefiles/')),
                ('type', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='basegpt.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('result', models.TextField(null=True)),
                ('type', models.CharField(blank=True, default='adtext', max_length=100, null=True)),
                ('user_rating', models.IntegerField(null=True)),
                ('all_count', models.IntegerField(null=True)),
                ('raw_all_count', models.IntegerField(null=True)),
                ('procent', models.IntegerField(null=True)),
                ('rating', models.IntegerField(null=True)),
                ('raw_procent', models.IntegerField(null=True)),
                ('raw_rating', models.IntegerField(null=True)),
                ('loops', models.IntegerField(null=True)),
                ('favorite', models.BooleanField(default=False)),
                ('input_tokens', models.IntegerField(null=True)),
                ('output_tokens', models.IntegerField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PromoCodeUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('used_at', models.DateTimeField(auto_now_add=True)),
                ('promo_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basegpt.promocode')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='promocode',
            name='used_by',
            field=models.ManyToManyField(through='basegpt.PromoCodeUsage', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='OrderTokens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('price', models.FloatField(null=True)),
                ('tokens', models.IntegerField(null=True)),
                ('transaction_id', models.CharField(max_length=100, null=True)),
                ('complete', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='promo_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='basegpt.promocode'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='InfoTextIterations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('rawtext', models.TextField(null=True)),
                ('raw_all_count', models.IntegerField(null=True)),
                ('raw_procent', models.IntegerField(null=True)),
                ('raw_rating', models.IntegerField(null=True)),
                ('textv1', models.TextField(null=True)),
                ('v1_all_count', models.IntegerField(null=True)),
                ('v1_procent', models.IntegerField(null=True)),
                ('v1_rating', models.IntegerField(null=True)),
                ('textv2', models.TextField(null=True)),
                ('v2_all_count', models.IntegerField(null=True)),
                ('v2_procent', models.IntegerField(null=True)),
                ('v2_rating', models.IntegerField(null=True)),
                ('textv3', models.TextField(null=True)),
                ('v3_all_count', models.IntegerField(null=True)),
                ('v3_procent', models.IntegerField(null=True)),
                ('v3_rating', models.IntegerField(null=True)),
                ('loops', models.IntegerField(null=True)),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basegpt.result')),
            ],
        ),
        migrations.CreateModel(
            name='ExamText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rawtext', models.TextField(null=True)),
                ('complete', models.BooleanField(default=False)),
                ('responsetext', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='basegpt.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contact_us',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
