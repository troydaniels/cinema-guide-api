"""
urls.py
Maps API queries to the relevant view

Troy Daniels - 05/06/16
"""

from django.conf.urls import url
from cinema_guide_api import views

urlpatterns = [
    url(r'^cinema/$', views.cinema_list),
    url(r'^movie/$', views.movie_list),
    url(r'^cinema/suburb/(?P<suburb>[^\/]+)/$', views.cinema_in_location),
    url(r'^cinema/(?P<identifier>[^\/]+)/(?P<date>[^\/]+)/$', views.cinema_on_date),
    url(r'^cinema/(?P<identifier>[^\/]+)/(?P<start>[^\/]+)/(?P<end>[^\/]+)/$', views.cinema_between_date),
    url(r'^cinema/(?P<identifier>[^\/]+)/$', views.cinema_detail),
    url(r'^movie/(?P<identifier>[^\/]+)/$', views.movie_detail)
]
