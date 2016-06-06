"""
test_models.py
Test a range of model properties on a series of test objects

Troy Daniels - 06/06/16
"""

import datetime
from django.test import TestCase
from cinema_guide_api.models import *

class modelTestCases(TestCase):
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
            name = "West Side Cinema",
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

    def test_cinemaTwo_address(self):
        """
        Test that cinemaTwos address is stored correctly
        """
        cinema = Cinema.objects.get(name="Eastern Flix")
        self.assertEqual(cinema.address.unit, None)
        self.assertEqual(cinema.address.street_name, "South Ave")
        self.assertEqual(cinema.address.postcode, "2000")

    def test_cinemaOne_showing_both_movies(self):
        """
        Test that cinemaOne is showing both movies, at the correct times
        """
        cinema = Cinema.objects.get(name = "West Side Cinema")
        self.assertEqual(cinema.movies.count(), 2)

        movieOne = Movie.objects.get(id = 1)
        movieTwo = Movie.objects.get(id = 2)
        self.assertEqual(movieOne.name, "The wild west")
        self.assertEqual(movieTwo.name, "The bassoonists father")
        self.assertEqual(Showing.objects.get(cinema=cinema, movie=movieOne).start, datetime.date(2016, 10, 1))
        self.assertEqual(Showing.objects.get(cinema=cinema, movie=movieOne).end, datetime.date(2016, 10, 30))
        self.assertEqual(Showing.objects.get(cinema=cinema, movie=movieTwo).end, None)

    def test_cinemaTwo_not_showing_movies(self):
        """
        Test that cinemaTwo is not currently showing any movies
        """
        cinema = Cinema.objects.get(name = "Eastern Flix")
        self.assertEqual(cinema.movies.count(), 0)
        
