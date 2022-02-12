from distutils.command.upload import upload
from lzma import FORMAT_ALONE
from operator import mod
from tabnanny import verbose
from venv import create
from django.db import models

from .managers import AvailableSession


class City(models.Model):
    """Модель городов"""
    name = models.CharField('Город', 
        max_length=100)
    slug = models.SlugField('Ссылка', max_length=100)
    movies = models.ManyToManyField('Movie',
        verbose_name='Фильмы')
    is_active = models.BooleanField('Активен', default=True)
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Movie(models.Model):
    """Модель фильмов"""
    
    AGE_CHOICES = (
        (0, '0+'),
        (1, '6+'),
        (2, '12+'),
        (3, '16+'),
        (4, '18+') 
    )
    objects = AvailableSession.as_manager()
    
    name = models.CharField('Название', max_length=100)
    age_limit = models.IntegerField('Ввозрастное ограничение', 
        choices=AGE_CHOICES)
    country = models.CharField('Страна', max_length=200)
    ganres = models.CharField('Жанры', max_length=200,
        null=True, blank=True)
    director = models.CharField('Режисер', max_length=200,
        null=True, blank=True)
    poster = models.ImageField('Постер', null=True, blank=True,
        upload_to='images/movies/%y/%m')
    memorandum = models.DateField('Меморандум', blank=True, null=True)
    description = models.TextField('Описание', blank=True, null=True)
    start_date = models.DateField('С даты')
    premier = models.BooleanField('Премьера', default=False)
    carousel = models.ImageField('Изображние для карусели',
        null=True, blank=True, upload_to='images/carousel/%y/%m' )
    trailer = models.FileField('Трейлер', null=True, blank=True)
    is_active = models.BooleanField('Активен', default=True)
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class Cinema(models.Model):
    """Модель кинотеатров"""
    name = models.CharField('Название кинотеатра', max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE,
        verbose_name='Город')
    information = models.TextField(default='Информация', 
        null=True, blank=True)
    is_active = models.BooleanField('Активен', default=True)
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Кинотеатр'
        verbose_name_plural = 'Кинотеатры'


class Session(models.Model):
    """Модель сеансов"""
    FORMAT_CHOICES = (
        ('1', '2D'),
        ('2', '3D'),
        ('3', 'IMAX')
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,
        verbose_name='Фильм')
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE,
        verbose_name='Кинотеатр')
    format = models.CharField('Формат', choices=FORMAT_CHOICES,
        max_length=10)
    date = models.DateField('Дата')
    time = models.TimeField('Время')
    is_active = models.BooleanField('Активен', default=True)
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.cinema.name} - {self.movie.name}'


    class Meta:
        verbose_name = 'Сеанс'
        verbose_name_plural = 'Сеансы'


