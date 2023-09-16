# Generated by Django 3.0.7 on 2023-09-16 05:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('prompt', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LikeDislike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(blank=True, db_index=True)),
                ('hidden', models.BooleanField(db_index=True, default=False)),
                ('trashed', models.BooleanField(db_index=True, default=False)),
                ('liked', models.BooleanField(default=True)),
                ('prompt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes_dislikes', to='prompt.Prompt')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
        ),
        migrations.AddConstraint(
            model_name='likedislike',
            constraint=models.UniqueConstraint(fields=('prompt', 'user'), name='unique_like_dislike'),
        ),
    ]
