# Generated by Django 5.1.5 on 2025-02-13 08:02

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("trains", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="train",
            options={"verbose_name": "Train", "verbose_name_plural": "Trains"},
        ),
    ]
