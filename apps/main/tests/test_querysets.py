from datetime import timedelta
from django.utils import timezone

import pytest 

from apps.main.models import Cinema, City, Movie, Session


class TestAvailbaMovieQuerySet:
    """Тесты фильтрации фильмов"""

    @pytest.fixture
    def city(self, db):
        return City.objects.create(name='one', slug='one')

    @pytest.fixture
    def movie1(self, db, city):
        now = timezone.now()
        movie =  Movie.objects.create(name='One', age_limit=0,
            country='Russia', start_date=timezone.now())
        city.movies.add(movie)
        cinema = Cinema.objects.create(name='One', city=city)
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

        return movie

    @pytest.fixture
    def movie2(self, db, city):
        now = timezone.now()
        movie =  Movie.objects.create(name='Two', age_limit=0,
            country='Russia', start_date=timezone.now())
        city.movies.add(movie)
        cinema = Cinema.objects.create(name='Two', city=city)

        Session.objects.create(
            movie=movie,
            cinema=cinema,
            format='1',
            date=now.date() + timezone.timedelta(days=1),
            time=(now + timezone.timedelta(hours=5)).time()
        )
        Session.objects.create(
            movie=movie,
            cinema=cinema,
            format='1',
            date=now.date() + timezone.timedelta(days=1),
            time=(now + timezone.timedelta(hours=2)).time()
        )
        
        return movie
    
    @pytest.fixture
    def movie3(self, db, city):
        now = timezone.now()
        movie = Movie.objects.create(name='Three', age_limit=0,
            country='Russia', start_date=timezone.now() + timezone.timedelta(days=1))
        city.movies.add(movie)
        cinema = Cinema.objects.create(name='Two', city=city)
        Session.objects.create(
            movie=movie,
            cinema=cinema,
            format='1',
            date=now.date() + timezone.timedelta(days=1),
            time=(now + timezone.timedelta(hours=2)).time()
        )
        return movie

    @pytest.fixture
    def movie4(self, db, city):
        now = timezone.now()
        movie = Movie.objects.create(name='Three', age_limit=0,
            country='Russia', start_date=timezone.now() + timezone.timedelta(days=1))
        city.movies.add(movie)
        cinema = Cinema.objects.create(name='Two', city=city)
        Session.objects.create(
            movie=movie,
            cinema=cinema,
            format='1',
            date=now.date() + timezone.timedelta(days=3),
            time=(now + timezone.timedelta(hours=2)).time()
        )
        return movie

    @pytest.mark.django_db
    def test_movies_today_queryset(self, city, movie1, movie2, movie3, movie4):
        movies_today = city.movies.movies_today()

        assert movies_today.count() == 1
        assert movies_today.first() == movie1

    @pytest.mark.django_db
    def test_movies_tomorrow_queryset(self, city, movie1, movie2, movie3, movie4):
        movies_tomorrow = city.movies.movies_tomorrow()

        assert movies_tomorrow.count() == 3
        assert movies_tomorrow.first() == movie1
        assert movies_tomorrow[1] == movie2
        assert movies_tomorrow[2] == movie3

    @pytest.mark.django_db
    def test_movies_soon_queryset(self, city, movie1, movie2, movie3, movie4):
        movies_soon = city.movies.movies_soon()

        assert movies_soon.count() == 2
        assert movies_soon.first() == movie3

    @pytest.mark.django_db
    def test_movies_date_queryset(self, city, movie1, movie2, movie3, movie4):
        date = timezone.now() + timezone.timedelta(days=3)
        movies_soon = city.movies.movies_date(date)

        assert movies_soon.count() == 1
        assert movies_soon.first() == movie4

    def test_movies_date_today_queryset(self, city,movie1, movie2, movie3, movie4):
        date = timezone.now()
        movies_soon = city.movies.movies_date(date)

        assert movies_soon.count() == 1
        assert movies_soon.first() == movie1