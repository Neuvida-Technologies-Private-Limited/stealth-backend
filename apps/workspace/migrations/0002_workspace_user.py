# Generated by Django 3.0.7 on 2023-09-17 18:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("workspace", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="workspace",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Author",
            ),
            preserve_default=False,
        ),
    ]
