from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from agro.models import Station, WeatherData, WeatherSummary
from api.serializers import WeatherSummarySerializer


class WeatherSummaryTests(APITestCase):

    def setUp(self):
        # create a station
        self.station = Station.objects.create(name='Test Station')

        # create some weather data
        WeatherData.objects.create(
            date='2022-01-01',
            station=self.station,
            max_temperature=50,
            min_temperature=40,
            precipitation=-9999
        )
        WeatherData.objects.create(
            date='2022-01-02',
            station=self.station,
            max_temperature=55,
            min_temperature=-9999,
            precipitation=15
        )

        WeatherData.objects.create(
            date='2022-01-03',
            station=self.station,
            max_temperature=-9999,
            min_temperature=45,
            precipitation=10
        )

        # create a weather summary
        WeatherSummary.objects.create(
            year=2022,
            station=self.station,
            avg_max_temp=52,
            avg_min_temp=42,
            total_precipitation=25
        )

    def test_get_weather_summary(self):
        url = reverse('weathersummary-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        expected_data = WeatherSummarySerializer(
            instance=WeatherSummary.objects.first()).data
        self.assertEqual(response.data[0], expected_data)
