import logging

from django.db import models

logger = logging.getLogger(__name__)


class Region(models.Model):
    name = models.CharField('Название', unique=True)


class City(models.Model):
    name = models.CharField('Название')
    region = models.ForeignKey('Region', verbose_name='Регион', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'region')


class Provider(models.Model):
    name = models.CharField('Название')
    inn = models.CharField('ИНН')

    class Meta:
        unique_together = ('name', 'inn')


class Range(models.Model):
    prefix = models.IntegerField('Префикс')
    number_from = models.IntegerField('Номер ОТ')
    number_to = models.IntegerField('Номер ДО')
    provider = models.ForeignKey('Provider', verbose_name='Провайдер', on_delete=models.CASCADE)
    city = models.ForeignKey('City', verbose_name='Город', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('prefix', 'number_from', 'number_to')
