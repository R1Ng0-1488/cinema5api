from nturl2path import url2pathname
from django.urls import path 

from . import views


urlpatterns = [
    path('cities/', views.CitiesView.as_view(), name='cities'),
    path('movies/<slug:city>/<str:type>/', 
        views.MoviesView.as_view(), name='movies'),
]
