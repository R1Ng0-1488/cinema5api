from attr import field
from rest_framework import serializers

from .models import City, Movie, Cinema, Session


class SessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Session
        exclude = ('created', 'updated')


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('name', 'slug')


class MovieSerializer(serializers.ModelSerializer):
    sessions_count = serializers.IntegerField(
        source='sessions.count', read_only=True
    )

    class Meta:
        model = Movie
        exclude = ('created', 'updated')