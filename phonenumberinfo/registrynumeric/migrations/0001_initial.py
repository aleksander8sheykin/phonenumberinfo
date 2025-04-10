# Generated by Django 5.2 on 2025-04-08 09:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Название')),
                ('inn', models.CharField(verbose_name='ИНН')),
            ],
            options={
                'unique_together': {('name', 'inn')},
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Название')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registrynumeric.region',
                                             verbose_name='Регион')),
            ],
            options={
                'unique_together': {('name', 'region')},
            },
        ),
        migrations.CreateModel(
            name='Range',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.IntegerField(verbose_name='Префикс')),
                ('number_from', models.IntegerField(verbose_name='Номер ОТ')),
                ('number_to', models.IntegerField(verbose_name='Номер ДО')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registrynumeric.city',
                                           verbose_name='Город')),
                ('provider',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registrynumeric.provider',
                                   verbose_name='Провайдер')),
            ],
            options={
                'unique_together': {('prefix', 'number_from', 'number_to')},
            },
        ),
    ]
