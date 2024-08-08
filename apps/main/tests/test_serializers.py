import pytest
from django.utils import timezone 
from django.core.files import File

from unittest import mock

from apps.main.models import City
from apps.main.serializers import CitySerializer, MovieSerializer


class TestCitySerializer:

    @pytest.fixture
    def data(self):
        return {
            'name': 'Оренбург',
            'slug': 'orenburg'
        }

    @pytest.fixture
    def invalid_data(self):
        return {'name': 'Щкутигкп'}

    @pytest.fixture
    def city(self, db):
        return City.objects.create(name='Оренбург', slug='orenburg')

    def test_fields_mutch(self, data):
        serializer = CitySerializer(data)
        assert set(serializer.data.keys()) == set(['name', 'slug'])

    def test_serializer_many(self, db, city, data):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        assert serializer.data == [data]

    def test_is_valid_false(self, db, city, data):
        serializer = CitySerializer(data=data)
        assert serializer.is_valid() is False 
        assert set(serializer.errors.keys()) == set(['name', 'slug'])
 
    def test_is_valid(self, db, city):
        serializer = CitySerializer(data={'name': 'One', 'slug': 'one'})
        assert serializer.is_valid() is True
        assert serializer.save()
        assert City.objects.count() == 2


class TestMovieSerializer:

    @pytest.fixture
    def data(self):
        now = timezone.now()
        poster = mock.MagicMock(spec=File, name='Poster')
        poster.name = 'Poster'   
        return {
            'name': 'One',
            'age_limit': 1,
            'country': 'Russia',
            'ganres': 'action',
            'director': 'John',
            'poster': poster,
            'start_date': now.date(),
            'memorandum': now.date(),
            'description': 'shit',
            'premier': False,
            'carousel': poster,
            'trailer': poster,
            'is_active': True,

        }

    def test_fields_mutch(self, data):
        serializer = MovieSerializer(data)
        assert set(serializer.data.keys()) == set(['name', 'age_limit', 'country', 'ganres', 'director', 
            'poster', 'memorandum', 'description', 'start_date', 'premier',
            'carousel', 'trailer', 'is_active'])

            