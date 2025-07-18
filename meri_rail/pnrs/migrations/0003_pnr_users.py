# Generated by Django 5.1.5 on 2025-02-14 06:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pnrs", "0002_alter_passengers_quota_alter_pnr_quota"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="pnr",
            name="users",
            field=models.ManyToManyField(
                related_name="pnrs", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
