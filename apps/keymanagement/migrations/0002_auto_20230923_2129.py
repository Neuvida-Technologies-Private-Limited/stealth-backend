# Generated by Django 3.0.7 on 2023-09-23 15:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("keymanagement", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="keymanagement",
            name="provider",
            field=models.CharField(
                choices=[("OpenAI", "OPENAI"), ("Bard", "BARD")],
                default="OpenAI",
                max_length=64,
            ),
        ),
        migrations.AlterField(
            model_name="keymanagement",
            name="title",
            field=models.TextField(default=""),
        ),
    ]
