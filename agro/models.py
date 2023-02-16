from django.db import models

# Create your models here.


class Station(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name'], name='unique_station_name')
        ]


class WeatherData(models.Model):
    date = models.DateField()
    station = models.ForeignKey(
        Station, on_delete=models.CASCADE,
        related_name="weather_data",
        to_field='name')
    max_temperature = models.IntegerField()
    min_temperature = models.IntegerField()
    precipitation = models.IntegerField()

    class Meta:
        unique_together = ('date', 'station')


class WeatherSummary(models.Model):
    year = models.IntegerField()
    station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="weather_summaries")
    avg_max_temp = models.IntegerField()
    avg_min_temp = models.IntegerField()
    total_precipitation = models.IntegerField()
