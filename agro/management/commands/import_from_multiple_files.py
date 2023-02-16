import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from agro.models import WeatherData, Station
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Imports weather data from all text files in a folder'

    def add_arguments(self, parser):
        parser.add_argument('folder_path', type=str,
                            help='Path to the folder containing the text files to import')

    def handle(self, *args, **kwargs):
        # configure the logger

        folder_path = kwargs['folder_path']
        # folder_path = os.path.join('agro', 'data')

        start_time = datetime.now()
        num_records_ingested = 0

        for file_name in os.listdir(folder_path):
            if file_name.endswith('.txt'):
                file_path = os.path.join(folder_path, file_name)

                station_name = file_path.split("/")[-1].split(".")[0]
                if not os.path.exists(file_path):
                    logging.error(f'File {file_path} does not exist')
                    return

                log_dir = os.path.join(
                    settings.BASE_DIR, 'logs-dirs', station_name)
                os.makedirs(log_dir, exist_ok=True)
                log_file = os.path.join(log_dir, f'{station_name}.log')
                logger.setLevel(logging.INFO)

                # Create a file handler and set its format
                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(logging.Formatter(
                    '%(asctime)s %(levelname)s %(message)s'))

                # Add the file handler to the logger
                logger.addHandler(file_handler)

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

                        weather_data = None

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
                            # imported_records += 1
                            logger.info(
                                f'Imported weather data for station {station_name} on {date}')
                        else:
                            logger.warning(
                                f'Duplicate weather data found for station {station_name} on {date}')

                    station.save()
                    if weather_data is not None:
                        weather_data.save()

        end_time = datetime.now()
        elapsed_time = end_time - start_time

        logger.info(f'Ingestion completed at {end_time}')
        logger.info(f'Elapsed time: {elapsed_time}')
        logger.info(f'Number of records ingested: {num_records_ingested}')

        self.stdout.write(self.style.SUCCESS(
            'Weather data imported successfully from all files in the folder!'))
