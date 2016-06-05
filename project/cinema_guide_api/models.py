import uuid
from django.db import models

class Address(models.Model):        
    unit = models.PositiveSmallIntegerField("Unit Number", blank = True)
    street = models.PositiveIntegerField("Street Number")
    suburb = models.CharField("Suburb", max_length = 50)
    state_province = models.CharField("State/Province", max_length = 40)
    postcode = models.CharField("Postal Code", max_length = 10)
    country = models.CharField("Country", max_length = 40)

class Movie(models.Model):
    name = models.CharField(max_length=100)
    #UUID as Movie ID & primary key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class Cinema(models.Model):
    name = models.CharField(max_length=100)
    #UUID as Cinema ID & primary key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.ForeignKey(Address, on_delete = models.CASCADE)
    #Use Showing model to store date info for Movie at Cinema
    movies = models.ManyToManyField(Movie, through = 'Showing')

class Showing(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete = models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)
    start = models.DateField("Start Date")
    end = models.DateField("End Date")
