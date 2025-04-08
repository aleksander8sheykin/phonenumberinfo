from django.test import TestCase
from django.urls import reverse

from registrynumeric.models import Range, Provider, City, Region


class RegistryApiTest(TestCase):

    def test_api(self):
        city = City.objects.create(name='г. Улан-Удэ', region=Region.objects.create(name='Республика Бурятия'))
        Range.objects.create(
            prefix=301,
            number_from=2180000,
            number_to=2189999,
            provider=Provider.objects.create(name='ПАО "Ростелеком"', inn='7707049388'),
            city=city,
        )
        Range.objects.create(
            prefix=301,
            number_from=2190000,
            number_to=2190499,
            provider=Provider.objects.create(name='АО "МТТ"', inn='7705017253'),
            city=city,
        )

        phonenumber = '73012180001'
        response = self.client.get(
            reverse('phonenumber-detail', args=(phonenumber,)),
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json(), {
            'provider': 'ПАО "Ростелеком"',
            'city': 'г. Улан-Удэ',
            'region': 'Республика Бурятия'
        })

        phonenumber = '73012190000'
        response = self.client.get(
            reverse('phonenumber-detail', args=(phonenumber,)),
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json(), {
            'provider': 'АО "МТТ"',
            'city': 'г. Улан-Удэ',
            'region': 'Республика Бурятия'
        })
