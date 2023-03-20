import datetime

from django.db import models
from django.utils import timezone

from services_app.models import Tariff
from user_app.models import UserProfile, Role


class House(models.Model):
    name = models.CharField(max_length=32, verbose_name='Название')
    address = models.CharField(max_length=128, verbose_name='Адрес')
    image_1 = models.ImageField(upload_to='house/', null=True, blank=True, verbose_name='Изображение 1')
    image_2 = models.ImageField(upload_to='house/', null=True, blank=True, verbose_name='Изображение 2')
    image_3 = models.ImageField(upload_to='house/', null=True, blank=True, verbose_name='Изображение 3')
    image_4 = models.ImageField(upload_to='house/', null=True, blank=True, verbose_name='Изображение 4')
    image_5 = models.ImageField(upload_to='house/', null=True, blank=True, verbose_name='Изображение 5')
    users = models.ManyToManyField(UserProfile, verbose_name='Пользователи')

    class Meta:
        verbose_name = 'Дом'
        verbose_name_plural = 'Дома'

    def __str__(self):
        return f"{self.name}"

class Section(models.Model):
    name = models.CharField(max_length=16, verbose_name='Название')
    house = models.ForeignKey(House, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Секция'
        verbose_name_plural = 'Секции'

    def __str__(self):
        return f"{self.name}"


class Floor(models.Model):
    name = models.CharField(max_length=16, verbose_name='Название')
    house = models.ForeignKey(House, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Этаж'
        verbose_name_plural = 'Этажи'

    def __str__(self):
        return f"{self.name}"


class Apartment(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='Секция')
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, verbose_name='Этаж')
    owner = models.ForeignKey(UserProfile, on_delete=models.PROTECT, null=True, blank=True, related_name='apartment',
                              verbose_name='Владелец')
    house = models.ForeignKey(House, null=True, on_delete=models.CASCADE)
    tariff = models.ForeignKey(Tariff, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Тариф')
    number = models.IntegerField(verbose_name='Номер квартиры')
    area = models.FloatField(null=True, blank=True, verbose_name='Площадь (кв.м.)')

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'
        unique_together = ['section', 'floor', 'number']

    def __str__(self):
        return f"{self.number}"

class Request(models.Model):
    CHOICES = (('new', 'Новое'),
               ('in_work', 'В работе'),
               ('done', 'Выполнено'))

    status = models.CharField(max_length=7, choices=CHOICES, default='new', verbose_name='Статус')
    date = models.DateField(default=datetime.date.today)
    time = models.TimeField()
    create_date = models.DateField(default=timezone.now)
    description = models.TextField()
    comment = models.TextField(blank=True)
    type_master = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)
    master = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.SET_NULL)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)