"""
views.py
Defines the views supported by the Cinema Guide API

Troy Daniels - 05/06/16
"""

import datetime
from rest_framework import status
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from cinema_guide_api.models import *
from cinema_guide_api.serializers import *

class JSONResponse(HttpResponse):
    """
    HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def cinema_list(request):
    """
    List all cinemas, or create a new cinema.
    """
    if request.method == 'GET':
        cinemas = Cinema.objects.all()
        serializer = CinemaSerializer(cinemas, many=True)
        return JSONResponse(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CinemaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def movie_list(request):
    """
    Allow the creation of a new movie.
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MovieSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def cinema_detail(request, identifier):
    """
    Retrieve, update or delete a cinema by name (case insensitive) or ID
    """
    try:
        #When identifier is not an int, will raise ValueError in this block
        #They will then be compared to cinema names (case insensitive)
        try:
            cinema = Cinema.objects.get(id = identifier)
        except ValueError:
            cinema = Cinema.objects.get(name__iexact = identifier)
    except Cinema.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CinemaSerializer(cinema)
        return JSONResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CinemaSerializer(cinema, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        else:
            return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        cinema.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    else:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def movie_detail(request, identifier):
    """
    Retrieve, update or delete a movie by name (case insensitive) or ID
    """
    try:
        #When identifier is not an int, will raise ValueError in this block
        #They will then be compared to movie names (case insensitive)
        try:
            movie = Movie.objects.get(id = identifier)
        except ValueError:
            movie = Movie.objects.get(name__iexact = identifier)
    except Movie.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return JSONResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = MovieSerializer(movie, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        movie.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    else:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def cinema_on_date(request, identifier, date):
    """
    Retrieve movies playing at a given cinema on a given date
    """
    try:
        #When identifier is not an int, will raise ValueError in this block
        #They will then be compared to cinema names (case insensitive)
        try:
            cinema = Cinema.objects.get(id = identifier)
        except ValueError:
            cinema = Cinema.objects.get(name__iexact = identifier)
    except Cinema.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        start = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        end = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        #The following is a JOIN query, on the Movie and Showing tables
        movies = Movie.objects.filter(showing__cinema = cinema, showing__start__lte = start, showing__end__gte = start)
        serializer = MovieSerializer(movies, many=True)
        return JSONResponse(serializer.data)
    else:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)

#TODO: Near duplicate function below - refactor
def cinema_between_date(request, identifier, start, end):
    """
    Retrieve movies playing at a given cinema between given dates
    """
    try:
        #When identifier is not an int, will raise ValueError in this block
        #They will then be compared to cinema names (case insensitive)
        try:
            cinema = Cinema.objects.get(id = identifier)
        except ValueError:
            cinema = Cinema.objects.get(name__iexact = identifier)
    except Cinema.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        st = datetime.datetime.strptime(start, '%Y-%m-%d').date()
        et = datetime.datetime.strptime(end, '%Y-%m-%d').date()
        #The following is a JOIN query, on the Movie and Showing tables
        movies = Movie.objects.filter(showing__cinema = cinema, showing__start__lte = st, showing__end__gte = et)
        serializer = MovieSerializer(movies, many=True)
        return JSONResponse(serializer.data)
    else:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def cinema_in_location(request, suburb):
    """
    Retrieves cinemas in a given suburb, case insensitively
    """
    if request.method == 'GET':
        #The following is a JOIN query on the Cinema and Address tables
        cinemas = Cinema.objects.filter(address__suburb__iexact=suburb)
        serializer = MovieSerializer(cinemas, many=True)
        return JSONResponse(serializer.data)
    else:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)

