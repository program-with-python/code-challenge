import django_filters
from agro.models import WeatherData, WeatherSummary
from django.db.models.functions import ExtractYear
from django.db import models


class WeatherDataFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(method='filter_by_year', label='Year')

    def filter_by_year(self, queryset, name, value):
        return queryset.annotate(year=ExtractYear('date')).filter(year=value)

    class Meta:
        model = WeatherData
        fields = {
            'date': ['exact'],
            'station__id': ['exact'],

        }

    filter_overrides = {
        models.DateField: {
            'filter_class': django_filters.DateFilter,
            'extra': lambda f: {
                'widget': forms.DateInput(attrs={'type': 'date'})
            }
        }
    }

    @property
    def qs(self):
        parent = super().qs
        if 'year' in self.form.data:
            return self.filter_by_year(parent, 'year', self.form.data['year'])
        return parent


class WeatherSummaryFilter(django_filters.FilterSet):
    class Meta:
        model = WeatherSummary
        fields = {
            'year': ['exact'],
            'station__id': ['exact'],
        }
