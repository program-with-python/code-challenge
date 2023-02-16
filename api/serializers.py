from rest_framework import serializers
from agro.models import WeatherData, Station, WeatherSummary


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'


class WeatherDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = WeatherData
        fields = '__all__'


class WeatherSummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = WeatherSummary
        fields = '__all__'
