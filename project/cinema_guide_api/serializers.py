from rest_framework import serializers
from cinema_guide_api.models import *

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('name', 'id')

class CinemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = ('name', 'id', 'address', 'movies')


