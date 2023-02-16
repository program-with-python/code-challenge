import pandas as pd
import numpy as np
from agro.models import WeatherSummary
import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
import logging
from agro.models import WeatherData, Station, WeatherSummary
from django.conf import settings


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Calculate weather summary for every year and station'

    def handle(self, *args, **kwargs):

        log_dir = os.path.join(settings.BASE_DIR, 'logs-dirs', 'analysis')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'analysis')
        logger.setLevel(logging.INFO)

        # Create a file handler and set its format
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s %(message)s'))

        # Add the file handler to the logger
        logger.addHandler(file_handler)

        # Get all the weather data
        weather_data = WeatherData.objects.all()

        # Convert weather data to a Pandas dataframe
        weather_df = pd.DataFrame(list(weather_data.values()))

        # Merge station data to the weather dataframe
        station_data = Station.objects.all()
        station_df = pd.DataFrame(list(station_data.values()))

        weather_df = weather_df.merge(
            station_df, left_on='station_id', right_on='name')

        # Convert the data to a Pandas DataFrame
        columns = ['date', 'max_temperature',
                   'min_temperature', 'precipitation', 'name']
        df = pd.DataFrame(weather_df, columns=columns)

        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        df['max_temperature'].replace(-9999, np.nan)

        df['max_temperature'] = df['max_temperature'].astype(int)

        df['min_temperature'] = df['min_temperature'].astype(int)

        df['precipitation'] = df['precipitation'].astype(int)

        # Group the data by year and station and calculate the averages and totals
        df_grouped = df.groupby([df['date'].dt.year, df.name])

        df_stats = df_grouped.agg({
            'max_temperature': lambda x: x[x != -9999].mean(skipna=True),
            'min_temperature': lambda x: x[x != -9999].mean(skipna=True),
            'precipitation': lambda x: x[x != -9999].sum(skipna=True),

        }).reset_index()

        # Calculate averages and totals
        summary_df = df_grouped.agg({
            'max_temperature': 'mean',
            'min_temperature': 'mean',
            'precipitation': 'sum'
        }).reset_index()

        # Convert temperature to Celsius
        summary_df['max_temperature'] = (
            summary_df['max_temperature'] - 32) * 5/9
        summary_df['min_temperature'] = (
            summary_df['min_temperature'] - 32) * 5/9

        # Log output indicating start and end times and number of records ingested
        start_time = weather_df['date'].min()
        end_time = weather_df['date'].max()
        num_records = len(weather_df.index)

        self.stdout.write(
            f'Successfully calculated and saved weather summary for {num_records} records between {start_time} and {end_time}')

        # Save the results to the WeatherStats model
        for index, row in df_stats.iterrows():

            year = row['date']
            station = Station.objects.get(name=row['name'])
            avg_max_temp = row['max_temperature']
            avg_min_temp = row['min_temperature']
            total_precip = row['precipitation']
            stats, created = WeatherSummary.objects.get_or_create(
                year=year,
                station=station,
                avg_max_temp=avg_max_temp,
                avg_min_temp=avg_min_temp,
                total_precipitation=total_precip
            )

            if created:
                logger.info(
                    f'Created new weather stats for {station} in {year}')
            else:
                logger.warning(
                    f'Duplicate weather stats found for {station} in {year}')

        self.stdout.write(self.style.SUCCESS(
            'Weather data imported successfully!'))
