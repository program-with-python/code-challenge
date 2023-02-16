import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from agro.models import WeatherData, Station
import os
from django.conf import settings

import logging


# Create a logger
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import weather data from .txt file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str,
                            help='Path to import data from text file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        station_name = file_path.split("/")[-1].split(".")[0]

        # station = Station.objects.get_or_create(name=station_name)

        log_dir = os.path.join(settings.BASE_DIR, 'logs', station_name)
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f'{station_name}.log')
        logger.setLevel(logging.INFO)

        # Create a file handler and set its format
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s %(message)s'))

        # Add the file handler to the logger
        logger.addHandler(file_handler)

        start_time = datetime.now()

        logger.info(f"Import started for file '{file_path}' at {start_time}")
        imported_records = 0

        with open(file_path, 'r') as file:
            reader = csv.reader(file, delimiter='\t')
            for row in reader:
                date_str = row[0].strip()
                date = datetime.strptime(date_str, '%Y%m%d')
                max_temp = int(row[1])
                min_temp = int(row[2])
                precipitation = int(row[3])
                station, created = Station.objects.get_or_create(
                    name=station_name)
                if created:
                    logger.info(f'Created new station: {station_name}')
                weather_data, created = WeatherData.objects.get_or_create(
                    date=date,
                    max_temperature=max_temp,
                    min_temperature=min_temp,
                    precipitation=precipitation,
                    station=station
                )
                if created:
                    imported_records += 1
                    logger.info(
                        f'Imported weather data for station {station_name} on {date}')
                else:
                    logger.warning(
                        f'Duplicate weather data found for station {station_name} on {date}')
        end_time = datetime.now()
        elapsed_time = end_time - start_time
        logger.info(
            f'Import completed in {elapsed_time}. Imported {imported_records} weather data records.')
        station.save()
        weather_data.save()

        logging.info(
            f"Imported {imported_records} weather data records for station {station_name}")

        self.stdout.write(self.style.SUCCESS(
            'Weather data imported successfully!'))
