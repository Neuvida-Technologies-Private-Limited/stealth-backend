# Generated by Django 3.0.7 on 2023-09-22 18:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_auto_20230922_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prompt',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
