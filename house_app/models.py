from django.db import models
from django.utils import timezone

from services_app.models import Tariff
from user_app.models import UserProfile



class Section(models.Model):
    name = models.CharField(max_length=16, verbose_name='Название')

    class Meta:
        verbose_name = 'Секция'
        verbose_name_plural = 'Секции'

    def __str__(self):
        return self.name


class Floor(models.Model):
    name = models.CharField(max_length=16, verbose_name='Название')

    class Meta:
        verbose_name = 'Этаж'
        verbose_name_plural = 'Этажи'

    def __str__(self):
        return self.name


class House(models.Model):
    name = models.CharField(max_length=32, verbose_name='Название')
    address = models.CharField(max_length=128, verbose_name='Адрес')
    image_1 = models.ImageField(upload_to='house/', null=True, blank=True, verbose_name='Изображение 1')
    image_2 = models.ImageField(upload_to='house/', null=True, blank=True, verbose_name='Изображение 2')
    image_3 = models.ImageField(upload_to='house/', null=True, blank=True, verbose_name='Изображение 3')
    image_4 = models.ImageField(upload_to='house/', null=True, blank=True, verbose_name='Изображение 4')
    image_5 = models.ImageField(upload_to='house/', null=True, blank=True, verbose_name='Изображение 5')
    sections = models.ManyToManyField(Section, verbose_name='Секции')
    floors = models.ManyToManyField(Floor, verbose_name='Этажи')
    users = models.ManyToManyField(UserProfile, verbose_name='Пользователи')

    class Meta:
        verbose_name = 'Дом'
        verbose_name_plural = 'Дома'

    def __str__(self):
        return self.name


class Apartment(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='Секция')
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, verbose_name='Этаж')
    owner = models.ForeignKey(UserProfile, on_delete=models.PROTECT, null=True, blank=True, related_name='apartment',
                              verbose_name='Владелец')
    tariff = models.ForeignKey(Tariff, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Тариф')
    number = models.IntegerField(verbose_name='Номер квартиры')
    area = models.FloatField(null=True, blank=True, verbose_name='Площадь (кв.м.)')

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'
        unique_together = ['section', 'floor', 'number']

    def __str__(self):
        return self.number