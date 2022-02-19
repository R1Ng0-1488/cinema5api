from urllib import response
import pytest
from django.urls import reverse
from pytest_django import asserts
from django.utils import timezone

from apps.main.models import City, Movie, Session, Cinema
from apps.main.serializers import MovieSerializer

class TestCitiesView:
    
    @pytest.fixture
    def cities(self, db):
        City.objects.create(name='zero', slug='zero', is_active=False)
        for i in ('one', 'two', 'three'):
            City.objects.create(name=i, slug=i)
        return City.objects.filter(is_active=True)

    def test_get_cities_return_200_status(self, db, client):
        response = client.get(reverse('cities'))
        assert response.status_code == 200

    def test_get_cities(self, db, client, cities):
        response = client.get(reverse('cities'))
        assert response.json() == [{'name': i.name, 'slug': i.slug} for i in cities]


class TestMoviesView:

    @pytest.fixture
    def city1(self, db):
        return City.objects.create(name='zero', slug='zero', is_active=True)

    @pytest.fixture
    def movies(self, db, city1):
        now = timezone.now()
        # 2 today and tomorrow
        movie =  Movie.objects.create(name='One', age_limit=0,
            country='Russia', start_date=timezone.now())
        cinema = Cinema.objects.create(name='One', city=city1)
        Session.objects.create(
            movie=movie,
            cinema=cinema,
            format='1',
            date=now.date(),
            time=(now + timezone.timedelta(hours=2)).time()
        )
        Session.objects.create(
            movie=movie,
            cinema=cinema,
            format='1',
            date=now.date(),
            time=(now + timezone.timedelta(hours=5)).time()
        )
        Session.objects.create(
            movie=movie,
            cinema=cinema,
            format='1',
            date=now.date() + timezone.timedelta(days=1),
            time=(now + timezone.timedelta(hours=5)).time()
        )
        # 2 tomorrow 
        movie2 =  Movie.objects.create(name='Two', age_limit=0,
            country='Russia', start_date=timezone.now())

        Session.objects.create(
            movie=movie2,
            cinema=cinema,
            format='1',
            date=now.date() + timezone.timedelta(days=1),
            time=(now + timezone.timedelta(hours=5)).time()
        )
        Session.objects.create(
            movie=movie2,
            cinema=cinema,
            format='1',
            date=now.date() + timezone.timedelta(days=1),
            time=(now + timezone.timedelta(hours=2)).time()
        )
        # tomorrow and soon
        movie3 = Movie.objects.create(name='Three', age_limit=0,
            country='Russia', start_date=timezone.now() + timezone.timedelta(days=1))
        cinema = Cinema.objects.create(name='Two', city=city1)
        Session.objects.create(
            movie=movie3,
            cinema=cinema,
            format='1',
            date=now.date() + timezone.timedelta(days=1),
            time=(now + timezone.timedelta(hours=2)).time()
        )
        city1.movies.add(movie)
        city1.movies.add(movie2)
        city1.movies.add(movie3)
        return Movie.objects.all()

    def test_get_movies_return_200(self, db, client, city1):
        response = client.get(
            reverse(
                'movies', 
                kwargs={
                    'city': city1.slug,
                    'type': 'today'
                }
            )
        )
        assert response.status_code == 200

    def test_get_movies_today(self, db, client, city1, movies):
        response = client.get(
            reverse(
                'movies', 
                kwargs={
                    'city': city1.slug,
                    'type': 'today'
                }
            )
        )
        assert len(response.json()) == movies.movies_today().count()
        assert response.json() == MovieSerializer(movies.movies_today(), many=True).data

    def test_get_movies_tomorrow(self, db, client, city1, movies):
        response = client.get(
            reverse(
                'movies', 
                kwargs={
                    'city': city1.slug,
                    'type': 'tomorrow',
                }
            )
        )
        assert len(response.json()) == movies.movies_tomorrow().count()
        assert response.json() == MovieSerializer(movies.movies_tomorrow(), many=True).data

    def test_get_movies_soon(self, db, client, city1, movies):
        response = client.get(
            reverse(
                'movies', 
                kwargs={
                    'city': city1.slug,
                    'type': 'soon',
                }
            )
        )
        assert len(response.json()) == movies.movies_soon().count()
        assert response.json() == MovieSerializer(movies.movies_soon(), many=True).data

    def test_get_movies_date(self, db, client, city1, movies):
        now = timezone.now()
        response = client.get(
            reverse(
                'movies_date', 
                kwargs={
                    'city': city1.slug,
                    'type': 'soon',
                    'date': now.strftime('%Y-%m-%d')
                }
            )
        )
        assert len(response.json()) == movies.movies_date(date=now).count()
        assert response.json() == MovieSerializer(movies.movies_date(date=now), many=True).data

    def test_with_wrong_parametr(self, db, client, city1):
        response = client.get(
            reverse(
                'movies',
                kwargs={
                    'city': city1.slug,
                    'type': 'kek',
                }
            )
        )
        assert response.json() == []

    def test_with_wrong_city(self, db, client):
        response = client.get(
            reverse(
                'movies',
                kwargs={
                    'city': 'Ordenburg',
                    'type': 'kek',
                }
            )
        )
        assert response.json() == []
