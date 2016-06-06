"""
test_views.py
Test a range of view properties on a selection of test objects

Troy Daniels - 06/06/16
"""

import datetime
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory
from cinema_guide_api.models import *
from cinema_guide_api.views import *

class viewTestCases(TestCase):
    def setUp(self):
        addressOne = Address.objects.create(
            unit = 1,
            street_number = 31,
            street_name = "West Ave",
            suburb = "Exampleville",
            state_province = "NSW",
            postcode = "2000",
            country = "Australia"
        )
        addressTwo = Address.objects.create(
            street_number = 100,
            street_name = "South Ave",
            suburb = "Otherville",
            state_province = "New South Wales",
            postcode = "2000",
            country = "Australia"
        )
        movieOne = Movie.objects.create(name = "The wild west")
        movieTwo = Movie.objects.create(name = "The bassoonists father")
        cinemaOne = Cinema.objects.create(
            name = "Western Cinema",
            address = addressOne,
        )
        cinemaTwo = Cinema.objects.create(
            name = "Eastern Flix",
            address = addressTwo,
        )
        #movieOne showing at cinemaOne from 1 October 2016 - 30 October 2016
        #Note YYYY-MM-DD format
        showingOne = Showing.objects.create(
            cinema = cinemaOne,
            movie = movieOne,
            start = "2016-10-01",
            end = "2016-10-30"
        )
        #movieTwo showing at cinemaOne from 12 September 2016 until an unspecified date
        #Note YYYY-MM-DD format
        showingTwo = Showing.objects.create(
            cinema = cinemaOne,
            movie = movieTwo,
            start = "2016-09-12"
        )

    def test_get_cinema_subfolder(self):
        """
        Test that a GET request to ~/cinema/ returns list of cinemas in JSON format
        """
        response = self.client.get('/cinema', follow = True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], "application/json")
        self.assertEqual(response.content, b'[{"name":"Western Cinema","id":1,"address":1,"movies":[1,2]},{"name":"Eastern Flix","id":2,"address":2,"movies":[]}]')

    def test_get_single_cinema_by_name(self):
        """
        Test that a GET request to ~/cinema/<name> returns correct cinema in valid JSON format
        """
        response = self.client.get('/cinema/Western%20Cinema', follow = True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], "application/json")
        self.assertEqual(response.content, b'{"name":"Western Cinema","id":1,"address":1,"movies":[1,2]}')

    def test_get_single_cinema_by_id(self):
        """
        Test that a GET request to ~/cinema/<id> returns correct cinema in valid JSON format
        """
        response = self.client.get('/cinema/1', follow = True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], "application/json")
        self.assertEqual(response.content, b'{"name":"Western Cinema","id":1,"address":1,"movies":[1,2]}')

    def test_get_single_movie_by_name(self):
        """
        Test that a GET request to ~/movie/<name> returns correct movie data in valid JSON format
        """
        response = self.client.get('/movie/The%20bassoonists%20father', follow = True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], "application/json")
        self.assertEqual(response.content, b'{"name":"The bassoonists father","id":2}')

    def test_get_single_movie_by_id(self):
        """
        Test that a GET request to ~/movie/<id> returns correct movie data in valid JSON format
        """
        response = self.client.get('/movie/2', follow = True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], "application/json")
        self.assertEqual(response.content, b'{"name":"The bassoonists father","id":2}')

    def test_get_movies_at_cinema(self):
        """
        Test that a GET request to ~/cinema/<name>/<date> returns the correct set of movies showing
        on that date at the given cinema
        """
        response = self.client.get('/cinema/1/2016-10-01', follow = True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], "application/json")
        self.assertEqual(response.content, b'[{"name":"The wild west","id":1}]')

    def test_get_cinemas_in_location(self):
        """
        Test that a GET request to ~/cinema/suburb/<suburb> returns the correct set of cinema listings
        for the given location
        """
        response = self.client.get('/cinema/suburb/otherville', follow = True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], "application/json")
        self.assertEqual(response.content, b'[{"name":"Eastern Flix","id":2}]')

    def test_get_movies_between_dates(self):
        """
        Tests that a GET request to ~/cinema/<id>/<start date>/<end date> returns the correct set of
        movie listings for the given cinema, between the given dates
        """
        response = self.client.get('/cinema/1/2016-10-01/2016-10-30', follow = True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], "application/json")
        self.assertEqual(response.content, b'[{"name":"The wild west","id":1}]')
