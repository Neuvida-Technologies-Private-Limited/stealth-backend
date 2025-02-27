# Generated by Django 3.0.7 on 2023-09-27 20:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workspace',
            name='hidden',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AddField(
            model_name='workspace',
            name='last_modified',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workspace',
            name='timestamp',
            field=models.DateTimeField(blank=True, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workspace',
            name='trashed',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
