from attr import field
from rest_framework import serializers

from .models import City, Movie, Cinema, Session


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('name', 'slug')


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        # fields = '__all__'
        exclude = ('created', 'updated')