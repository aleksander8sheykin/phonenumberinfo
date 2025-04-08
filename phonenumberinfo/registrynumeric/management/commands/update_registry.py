import csv
import logging

import requests
from django.core.management import BaseCommand
from django.db import transaction

from registrynumeric.models import Range, Provider, City, Region

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        # https://opendata.digital.gov.ru/registry/numeric/downloads/
        # https://opendata.digital.gov.ru/downloads/ABC-3xx.csv?1710948258581
        archive_urls = [
            'https://opendata.digital.gov.ru/downloads/ABC-3xx.csv',
            'https://opendata.digital.gov.ru/downloads/ABC-4xx.csv',
            'https://opendata.digital.gov.ru/downloads/ABC-8xx.csv',
            'https://opendata.digital.gov.ru/downloads/DEF-9xx.csv'
        ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }

        readers = []
        logger.info('Start reading')
        for url in archive_urls:
            response = requests.get(url, headers=headers)
            reader = csv.reader(response.content.decode().splitlines(), delimiter=';')
            readers.append(reader)
            logger.info(f'Read {url}')

        Range.objects.all().delete()

        regions, cities, providers = {}, {}, {}

        for reader in readers:
            logger.info(f'Start loading next readers')
            next(reader)  # skip first line with titles
            for row in reader:
                (prefix, number_from, number_to, _, provider_name, city_region, _, inn) = row

                prefix, number_from, number_to = int(prefix), int(number_from), int(number_to)

                try:
                    city_name, region_name = city_region.split('|', 1)
                except ValueError:  # city_region = 'Ставропольский край'
                    city_name = region_name = city_region

                region = regions.setdefault(
                    region_name,
                    Region.objects.get_or_create(name=region_name)[0]
                )

                city = cities.setdefault(
                    city_region,
                    City.objects.get_or_create(name=city_name, region=region)[0]
                )

                provider = providers.setdefault(
                    f'{provider_name}|{inn}',
                    Provider.objects.get_or_create(name=provider_name, inn=inn)[0]
                )

                Range.objects.update_or_create(
                    prefix=prefix,
                    number_from=number_from,
                    number_to=number_to,
                    provider=provider,
                    city=city,
                )
