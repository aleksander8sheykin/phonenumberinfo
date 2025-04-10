import csv
import logging
import typing

import requests
from django.core.management import BaseCommand
from django.db import transaction

from registrynumeric import models

logger = logging.getLogger(__name__)

ARCHIVE_URLS = [
    'https://opendata.digital.gov.ru/downloads/ABC-3xx.csv',
    'https://opendata.digital.gov.ru/downloads/ABC-4xx.csv',
    'https://opendata.digital.gov.ru/downloads/ABC-8xx.csv',
    'https://opendata.digital.gov.ru/downloads/DEF-9xx.csv',
]
INSERT_BATCH_SIZE = 1000


class Command(BaseCommand):
    class GetNextReader:
        def __init__(self, urls: list[str]):
            self.urls = urls[::]
            self.idx = 0
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
            }

        def __iter__(self):
            return self

        def __next__(self):
            self.idx += 1
            if self.idx >= len(self.urls):
                raise StopIteration
            response = requests.get(self.urls[self.idx], headers=self.headers)
            return csv.reader(response.content.decode().splitlines(), delimiter=';')

    @transaction.atomic
    def handle(self, *args, **options):

        models.Range.objects.all().delete()

        regions: typing.Dict[str, models.Region] = {}
        cities: typing.Dict[str, models.City] = {}
        providers: typing.Dict[str, models.Provider] = {}

        readers = self.GetNextReader(ARCHIVE_URLS)

        batch_insert = []
        for reader in readers:
            logger.info(f'Start loading next readers')
            _ = next(reader)  # skip first line with titles

            for row in reader:
                prefix = int(row[0])
                number_from = int(row[1])
                number_to = int(row[2])
                provider_name = row[4]
                city_region = row[5]
                inn = row[7]

                try:
                    city_name, region_name = city_region.split('|', 1)
                except ValueError:  # city_region = 'Ставропольский край'
                    city_name = region_name = city_region

                region: models.Region = regions.setdefault(
                    region_name,
                    models.Region.objects.get_or_create(name=region_name)[0]
                )

                city: models.City = cities.setdefault(
                    city_region,
                    models.City.objects.get_or_create(name=city_name, region=region)[0]
                )

                provider: models.Provider = providers.setdefault(
                    f'{provider_name}|{inn}',
                    models.Provider.objects.get_or_create(name=provider_name, inn=inn)[0]
                )

                batch_insert.append(
                    models.Range(
                        prefix=prefix,
                        number_from=number_from,
                        number_to=number_to,
                        provider=provider,
                        city=city,
                    )
                )
                if len(batch_insert) >= INSERT_BATCH_SIZE:
                    models.Range.objects.bulk_create(batch_insert, ignore_conflicts=True)
                    batch_insert.clear()

        models.Range.objects.bulk_create(batch_insert, ignore_conflicts=True)
