from django.http import HttpResponse
from django.db.models import Q
#TODO: update the following to use token authentication
from django.views.decorators.csrf import csrf_exempt
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

@csrf_exempt
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
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def cinema_detail(request, identifier):
    """
    Retrieve, update or delete a cinema by name/id.
    """
    try:
        cinema = Cinema.objects.get(
            Q(name=identifier) | Q(id=identifier)
        )
    except Cinema.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CinemaSerializer(cinema)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CinemaSerializer(cinema, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        cinema.delete()
        return HttpResponse(status=204)

@csrf_exempt
def movie_detail(request, identifier):
    """
    Retrieve, update or delete a movie by name/id.
    """
    try:
        movie = Movie.objects.get(
             Q(name=identifier) | Q(id=identifier)
        )         
    except Movie.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = MovieSerializer(movie, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        movie.delete()
        return HttpResponse(status=204)

