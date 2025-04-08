from unittest import mock

from django.core.management import call_command
from django.test import TestCase
from requests import Response

from registrynumeric.models import Range, Provider, City, Region

test_data = """АВС/ DEF;От;До;Емкость;Оператор;Регион;Территория ГАР;ИНН
301;2110000;2129999;20000;ПАО "Ростелеком";г. Улан-Удэ|Республика Бурятия;г. Улан-Удэ|г.о. город Улан-Удэ|Республика Бурятия;7707049388
301;2150000;2169999;20000;ПАО "Ростелеком";г. Улан-Удэ|Республика Бурятия;г. Улан-Удэ|г.о. город Улан-Удэ|Республика Бурятия;7707049388
301;2180000;2189999;10000;ПАО "Ростелеком";г. Улан-Удэ|Республика Бурятия;г. Улан-Удэ|г.о. город Улан-Удэ|Республика Бурятия;7707049388
301;2190000;2190499;500;АО "МТТ";г. Улан-Удэ|Республика Бурятия;г. Улан-Удэ|г.о. город Улан-Удэ|Республика Бурятия;7705017253
301;2191000;2199999;9000;ПАО "Ростелеком";г. Улан-Удэ|Республика Бурятия;г. Улан-Удэ|г.о. город Улан-Удэ|Республика Бурятия;7707049388
383;2855484;2855485;2;АО "ЭР-ТЕЛЕКОМ ХОЛДИНГ";г. Новосибирск|Новосибирская обл.;г. Новосибирск|г.о. город Новосибирск|Новосибирская область;5902202276
383;2855486;2855487;2;АО "ЭР-ТЕЛЕКОМ ХОЛДИНГ";г. Новосибирск|Новосибирская обл.;г. Новосибирск|г.о. город Новосибирск|Новосибирская область;5902202276
383;2855488;2855488;1;АО "ЭР-ТЕЛЕКОМ ХОЛДИНГ";г. Новосибирск|Новосибирская обл.;г. Новосибирск|г.о. город Новосибирск|Новосибирская область;5902202276
383;2855489;2855489;1;ООО "НОВОТЕЛЕКОМ";г. Новосибирск|Новосибирская обл.;г. Новосибирск|г.о. город Новосибирск|Новосибирская область;5406260827
383;2855490;2855490;1;АО "ЭР-ТЕЛЕКОМ ХОЛДИНГ";г. Новосибирск|Новосибирская обл.;г. Новосибирск|г.о. город Новосибирск|Новосибирская область;5902202276
"""


class RegistryLoaderTest(TestCase):

    def test_loader(self):
        resp = Response()
        resp.status_code = 200
        resp._content = str.encode(test_data)

        with mock.patch('requests.get', return_value=resp):
            call_command('update_registry')

            self.assertEqual(4, Provider.objects.count())
            self.assertEqual(2, City.objects.count())
            self.assertEqual(2, Region.objects.count())
            self.assertEqual(4, Provider.objects.count())
            self.assertEqual(10, Range.objects.count())

            range_one = Range.objects.get(prefix=383, number_from=2855486, number_to=2855487)
            self.assertEqual(range_one.city.name, 'г. Новосибирск')
            self.assertEqual(range_one.city.region.name, 'Новосибирская обл.')
            self.assertEqual(range_one.provider.name, 'АО "ЭР-ТЕЛЕКОМ ХОЛДИНГ"')
            self.assertEqual(range_one.provider.inn, '5902202276')
