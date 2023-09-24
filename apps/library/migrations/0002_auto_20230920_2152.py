# Generated by Django 3.0.7 on 2023-09-20 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("library", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="parametermapping",
            name="parameter",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="library.Parameter",
            ),
        ),
        migrations.AlterField(
            model_name="model",
            name="name",
            field=models.CharField(
                choices=[("OpenAI", "OPENAI"), ("Bard", "BARD")],
                max_length=255,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="prompt",
            name="prompt_type",
            field=models.CharField(
                choices=[("Chat", "CHAT"), ("Completion", "COMPLETION")],
                max_length=255,
                unique=True,
            ),
        ),
    ]
