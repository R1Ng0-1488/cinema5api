from django.utils import timezone
from django.core.exceptions import ValidationError

import pytest 

from apps.main.models import City, Movie, Session


class TestCityModel:
    """Тест модели города"""

    def create_initial(self):
        return City.objects.create(name='One', slug='one')
    
    def test_name_cannot_bo_more_then_100_letters(self):
        city = City(name='a'*101, slug='one')
        with pytest.raises(ValidationError):
            city.full_clean()

    def test_slug_cannot_bo_more_then_100_letters(self):
        city = City(slug='a'*101, name='one')
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