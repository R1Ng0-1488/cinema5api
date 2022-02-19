from rest_framework.generics import ListAPIView 

from .utils import convert_date
from .models import City, Movie
from .serializers import CitySerializer, MovieSerializer


class CitiesView(ListAPIView):
    serializer_class = CitySerializer

    def get_queryset(self):
        return City.objects.filter(is_active=True)


class MoviesView(ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        try:
            city = City.objects.get(slug=self.kwargs.get('city'))
            date = self.kwargs.get('date') 
            if date:
                return city.movies.movies_date(
                    date=convert_date(date)
                )
            return getattr(city.movies, f'movies_{self.kwargs.get("type")}')()
        except Exception as e:
            return None