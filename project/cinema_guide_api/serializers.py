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


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('unit', 'street_number', 'street_name', 'suburb', 'state_province', 'postcode', 'country')

class ShowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Showing
        fields = ('cinema', 'movie', 'start', 'end')
