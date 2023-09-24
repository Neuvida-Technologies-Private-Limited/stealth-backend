# Generated by Django 3.0.7 on 2023-09-20 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("workspace", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Model",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField(blank=True, db_index=True)),
                ("hidden", models.BooleanField(db_index=True, default=False)),
                ("trashed", models.BooleanField(db_index=True, default=False)),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                (
                    "name",
                    models.CharField(
                        choices=[("Open AI", "OPENAI"), ("Bard", "BARD")],
                        max_length=255,
                        unique=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Parameter",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField(blank=True, db_index=True)),
                ("hidden", models.BooleanField(db_index=True, default=False)),
                ("trashed", models.BooleanField(db_index=True, default=False)),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("temperature", "TEMPERATURE"),
                            ("maximum_length", "MAXIMUM_LENGTH"),
                            ("stop_sequence", "STOP_SEQUENCE"),
                            ("top_p", "TOP_P"),
                            ("frequency_penalty", "FREQUENCY_PENALTY"),
                            ("presence_penalty", "PRESENCE_PENALTY"),
                            ("logit_bias", "LOGIT_BIAS"),
                        ],
                        max_length=255,
                        unique=True,
                    ),
                ),
                ("description", models.TextField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Prompt",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField(blank=True, db_index=True)),
                ("hidden", models.BooleanField(db_index=True, default=False)),
                ("trashed", models.BooleanField(db_index=True, default=False)),
                ("title", models.CharField(max_length=255)),
                ("system_message", models.TextField()),
                ("user_message", models.TextField()),
                ("sample_output", models.TextField()),
                ("bookmarked", models.BooleanField(default=False)),
                ("published", models.BooleanField(default=False)),
                ("is_public", models.BooleanField(default=False)),
                (
                    "prompt_type",
                    models.CharField(
                        choices=[("CHAT", "CHAT"), ("Completion", "COMPLETION")],
                        max_length=255,
                        unique=True,
                    ),
                ),
                (
                    "workspace",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="prompts",
                        to="workspace.Workspace",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PromptOutput",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField(blank=True, db_index=True)),
                ("hidden", models.BooleanField(db_index=True, default=False)),
                ("trashed", models.BooleanField(db_index=True, default=False)),
                ("output", models.TextField()),
                (
                    "prompt",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="library.Prompt",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ParameterMapping",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField(blank=True, db_index=True)),
                ("hidden", models.BooleanField(db_index=True, default=False)),
                ("trashed", models.BooleanField(db_index=True, default=False)),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("value", models.CharField(max_length=256)),
                (
                    "model",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="library.Model",
                    ),
                ),
                (
                    "prompt",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="library.Prompt",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="LikeDislikePrompt",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField(blank=True, db_index=True)),
                ("hidden", models.BooleanField(db_index=True, default=False)),
                ("trashed", models.BooleanField(db_index=True, default=False)),
                ("liked", models.BooleanField(default=True)),
                (
                    "prompt",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="likes_dislikes",
                        to="library.Prompt",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Author",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="likedislikeprompt",
            constraint=models.UniqueConstraint(
                fields=("prompt", "user"), name="unique_like_dislike"
            ),
        ),
    ]
