from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.core.files import File

from unittest import mock
import pytest 

from apps.main.models import Cinema, City, Movie, Session


class TestCityModel:
    """Тесты модели Города"""

    def create_initial(self):
        return City.objects.create(name='One', slug='one')
    
    def test_name_cannot_bo_more_then_100_letters(self, db):
        city = City(name='a' * 101, slug='one')
        with pytest.raises(ValidationError):
            city.full_clean()

    def test_slug_cannot_bo_more_then_100_letters(self, db):
        city = City(slug='b' * 101, name='one1')
        with pytest.raises(ValidationError):
            city.full_clean()

    def test_str_output(self):
        city = City(name='one')
        assert str(city) == city.name
    
    @pytest.mark.django_db
    def test_city_can_have_movies(self):
        movie = Movie.objects.create(name='One', age_limit=0,
            country='Russia', start_date=timezone.now())
        city = self.create_initial()
        city.movies.add(movie)
        assert city.movies.first().id == movie.id
    
    def test_city_default_values(self):
        city = City(name='one')
        assert city.is_active is True

    @pytest.mark.django_db
    def test_city_name_unique(self):
        City.objects.create(name='one', slug='one')
        with pytest.raises(IntegrityError):
            City.objects.create(name='one', slug='one')


class TestMovieModel:
    """Тесты модели Фильмы"""

    def initial_movie(self, now):
        return Movie(
            name='One', age_limit=1, 
            country='Russia',
            start_date=now
        )
    
    def test_match_values(self):
        poster = mock.MagicMock(spec=File, name='Poster')
        poster.name = 'Poster'       
        carousel = mock.MagicMock(spec=File, name='Carousel')
        carousel.name = 'Carousel'
        now = timezone.now()
        movie = self.initial_movie(now)
        movie.ganres = 'Horror'
        movie.director = 'James Cameron'
        movie.memorandum = now
        movie.description = 'Something'
        movie.poster = poster
        movie.carousel = carousel
        assert movie.poster == poster
        assert movie.carousel == carousel
        assert movie.ganres == 'Horror'
        assert movie.director == 'James Cameron'
        assert movie.memorandum == now
        assert movie.name == 'One'
        assert movie.age_limit == 1
        assert movie.country == 'Russia'
        assert movie.start_date == now

    def test_match_default_values(self):
        now = timezone.now()
        movie = self.initial_movie(now)
        assert movie.premier is False
        assert movie.is_active is True

    def test_name_cannot_bo_more_then_100_letters(self):
        now = timezone.now()
        movie = self.initial_movie(now)
        movie.name = 'a'*101
        with pytest.raises(ValidationError):
            movie.full_clean()

    @pytest.mark.django_db
    def test_fields_can_be_blank(self):
        now = timezone.now()
        movie = self.initial_movie(now)
        movie.save()
        movie.full_clean()

    def test_country_cannot_be_more_then_200_letters(self):
        now = timezone.now()
        movie = self.initial_movie(now)
        movie.country = 'a' * 201
        with pytest.raises(ValidationError):
            movie.full_clean()

    def test_ganres_cannot_be_more_then_200_letters(self):
        now = timezone.now()
        movie = self.initial_movie(now)
        movie.ganres = 'a' * 201
        with pytest.raises(ValidationError):
            movie.full_clean()

    def test_director_cannot_be_more_then_200_letters(self):
        now = timezone.now()
        movie = self.initial_movie(now)
        movie.director = 'a' * 201
        with pytest.raises(ValidationError):
            movie.full_clean()

    def test_str_view(self):
        now = timezone.now()
        movie = self.initial_movie(now)
        assert str(movie) == 'One'


class TestCinemaModel:
    """Тесты модели Кинотеатров"""

    def initial_cinema(self):
        self.city = City.objects.create(name='One', slug='one')
        return Cinema(name='One', city=self.city)

    @pytest.mark.django_db
    def test_match_values(self):
        cinema = self.initial_cinema()
        cinema.information = 'something'

        assert cinema.name == 'One'
        assert cinema.city == self.city
        assert cinema.is_active is True

    @pytest.mark.django_db
    def test_name_cannot_be_more_then_200_letters(self):
        cinema = self.initial_cinema()
        cinema.name = 'a' * 201

        with pytest.raises(ValidationError):
            cinema.full_clean()

    def test_str_view(self):
        cinema = Cinema(name='One')
        assert str(cinema) == 'One'


class TestSessionModel:
    """Тесты модели Сеансов"""

    def initial_session(self):
        self.now = timezone.now()
        self.city = City.objects.create(name='One', slug='one')
        self.cinema = Cinema.objects.create(name='One', city=self.city)
        self.movie = Movie.objects.create(
            name='One', age_limit=1, 
            country='Russia',
            start_date=self.now
        )
        return Session.objects.create(
            movie=self.movie,
            cinema=self.cinema,
            format='1',
            date=self.now.date(),
            time=self.now.time()
        )

    @pytest.mark.django_db
    def test_value_match(self):
        session = self.initial_session()

        assert session.movie == self.movie
        assert session.cinema == self.cinema
        assert session.format == '1'
        assert session.date == self.now.date()
        assert session.time == self.now.time()
        assert session.is_active is True

    @pytest.mark.django_db
    def test_str_view(self):
        session = self.initial_session()
        assert str(session) == f'{self.cinema.name} - {self.movie.name}'