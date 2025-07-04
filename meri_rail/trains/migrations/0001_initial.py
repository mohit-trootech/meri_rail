# Generated by Django 5.1.5 on 2025-02-04 13:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("stations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Train",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number", models.CharField(max_length=5, unique=True)),
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name": "Train",
                "verbose_name_plural": "Trains",
                "ordering": ("number",),
            },
        ),
        migrations.CreateModel(
            name="Schedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("monday", models.CharField(blank=True, max_length=10, null=True)),
                ("tuesday", models.CharField(blank=True, max_length=10, null=True)),
                ("wednesday", models.CharField(blank=True, max_length=10, null=True)),
                ("thursday", models.CharField(blank=True, max_length=10, null=True)),
                ("friday", models.CharField(blank=True, max_length=10, null=True)),
                ("saturday", models.CharField(blank=True, max_length=10, null=True)),
                ("sunday", models.CharField(blank=True, max_length=10, null=True)),
                (
                    "train",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="schedule",
                        to="trains.train",
                    ),
                ),
            ],
            options={
                "verbose_name": "Schedule",
                "verbose_name_plural": "Schedule",
            },
        ),
        migrations.CreateModel(
            name="Route",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("route_number", models.CharField(max_length=3)),
                ("halt", models.CharField(blank=True, max_length=10, null=True)),
                ("day_count", models.IntegerField(blank=True, null=True)),
                ("platform", models.IntegerField(blank=True, null=True)),
                ("arrival", models.TimeField(blank=True, null=True)),
                ("departure", models.TimeField(blank=True, null=True)),
                (
                    "station",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="route",
                        to="stations.station",
                    ),
                ),
                (
                    "train",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="route",
                        to="trains.train",
                    ),
                ),
            ],
            options={
                "verbose_name": "Route",
                "verbose_name_plural": "Route",
            },
        ),
        migrations.CreateModel(
            name="TrainDetail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("distance", models.CharField(blank=True, max_length=32, null=True)),
                (
                    "station_from",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="station_from",
                        to="stations.station",
                    ),
                ),
                (
                    "station_to",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="station_to",
                        to="stations.station",
                    ),
                ),
                (
                    "train",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="details",
                        to="trains.train",
                    ),
                ),
            ],
            options={
                "verbose_name": "Train Detail",
                "verbose_name_plural": "Train Detail",
            },
        ),
    ]
