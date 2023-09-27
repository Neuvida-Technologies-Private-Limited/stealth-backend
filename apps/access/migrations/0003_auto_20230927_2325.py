# Generated by Django 3.0.7 on 2023-09-27 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0002_auto_20230924_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='reset_password_token',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
    ]
