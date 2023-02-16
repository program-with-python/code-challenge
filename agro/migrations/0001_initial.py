# Generated by Django 4.1.6 on 2023-02-16 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Station",
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
                ("name", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="WeatherSummary",
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
                ("year", models.IntegerField()),
                ("avg_max_temp", models.IntegerField()),
                ("avg_min_temp", models.IntegerField()),
                ("total_precipitation", models.IntegerField()),
                (
                    "station",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="weather_summaries",
                        to="agro.station",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WeatherData",
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
                ("date", models.DateField()),
                ("max_temperature", models.IntegerField()),
                ("min_temperature", models.IntegerField()),
                ("precipitation", models.IntegerField()),
                (
                    "station",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="weather_data",
                        to="agro.station",
                        to_field="name",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="station",
            constraint=models.UniqueConstraint(
                fields=("name",), name="unique_station_name"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="weatherdata", unique_together={("date", "station")},
        ),
    ]
