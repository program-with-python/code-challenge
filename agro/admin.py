from django.contrib import admin
from agro.models import WeatherData, WeatherSummary, Station

admin.site.register(WeatherData)
admin.site.register(WeatherSummary)
admin.site.register(Station)
