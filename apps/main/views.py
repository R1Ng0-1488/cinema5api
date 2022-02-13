from rest_framework.generics import ListAPIView

from .models import City, Movie
from .serializers import CitySerializer, MovieSerializer


class CitiesView(ListAPIView):
    serializer_class = CitySerializer

    def get_queryset(self):
        return City.objects.filter(is_active=True)


class MoviesView(ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        city = City.objects.get(slug=self.kwargs.get('city'))
        return city.movies.movies_today()
