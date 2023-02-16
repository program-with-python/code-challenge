from django.test import TestCase, RequestFactory
from rest_framework.test import APIRequestFactory
from api.views import WeatherDataViewSet


class TestWeatherDataViewSet(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = WeatherDataViewSet.as_view({'get': 'list'})

    def test_list_weather_data(self):
        # Create a test request
        request = self.factory.get('/api/weather/')

        # Call the view
        response = self.view(request)

        # Check that the response code is 200
        self.assertEqual(response.status_code, 200)

        # Check that the response data is not empty
        self.assertNotEqual(response.data, [])
