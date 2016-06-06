from django.conf.urls import url
from cinema_guide_api import views

urlpatterns = [
    url(r'^cinema/$', views.cinema_list),
    url(r'^cinema/(?P<identifier>.+)/', views.cinema_detail),
    url(r'^movie/(?P<identifier>.+)/', views.movie_detail),
]
