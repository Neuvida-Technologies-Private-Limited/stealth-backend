# Generated by Django 3.0.7 on 2023-10-05 17:14

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('keymanagement', '0003_auto_20230924_0039'),
    ]

    operations = [
        migrations.AddField(
            model_name='keymanagement',
            name='hidden',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AddField(
            model_name='keymanagement',
            name='timestamp',
            field=models.DateTimeField(blank=True, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='keymanagement',
            name='trashed',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
