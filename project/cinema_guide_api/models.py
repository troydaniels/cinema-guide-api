from django.db import models

class Address(models.Model):        
    unit = models.PositiveSmallIntegerField("Unit Number", null = True, blank = True)
    street_number = models.PositiveIntegerField("Street Number")
    street_name = models.CharField("Street Name", max_length = 50)
    suburb = models.CharField("Suburb", max_length = 50)
    state_province = models.CharField("State/Province", max_length = 40)
    postcode = models.CharField("Postcode", max_length = 10)
    country = models.CharField("Country", max_length = 40)

class Movie(models.Model):
    name = models.CharField("Movie Name", max_length=100)
    id = models.AutoField("Movie ID", primary_key=True)

class Cinema(models.Model):
    name = models.CharField("Cinema Name", max_length=100)
    address = models.ForeignKey(Address, on_delete = models.CASCADE)
    id = models.AutoField("Cinema ID", primary_key=True)
    #Use Showing model to store date info for Movie at Cinema
    movies = models.ManyToManyField(Movie, through = 'Showing', blank = True)

class Showing(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete = models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)
    #Movies need not start (ie, 'coming soon') nor finish date
    start = models.DateField("Start Date", null = True, blank = True)
    end = models.DateField("End Date", null = True, blank = True)
