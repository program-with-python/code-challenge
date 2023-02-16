from rest_framework import generics
from rest_framework.response import Response
from rest_framework import viewsets
from agro.models import Station, WeatherData, WeatherSummary
from api.serializers import StationSerializer, WeatherDataSerializer, WeatherSummarySerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import WeatherDataFilter


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class WeatherDataPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class WeatherDataViewSet(viewsets.ModelViewSet):
    queryset = WeatherData.objects.all().order_by('id')
    serializer_class = WeatherDataSerializer
    pagination_class = WeatherDataPagination
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['date', 'station']
    filterset_class = WeatherDataFilter


class WeatherSummaryViewSet(viewsets.ModelViewSet):
    queryset = WeatherSummary.objects.all().order_by('id')
    serializer_class = WeatherSummarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['year', 'station']
