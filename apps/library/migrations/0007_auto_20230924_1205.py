# Generated by Django 3.0.7 on 2023-09-24 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("library", "0006_auto_20230923_2048"),
    ]

    operations = [
        migrations.AlterField(
            model_name="parametermapping",
            name="prompt",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="library.Prompt",
            ),
        ),
        migrations.AlterField(
            model_name="promptoutput",
            name="prompt",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="prompt_output",
                to="library.Prompt",
            ),
        ),
    ]
