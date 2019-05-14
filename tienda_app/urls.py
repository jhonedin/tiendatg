from django.urls import path, include
from . import views
import string

urlpatterns = [
    path('home/', views.Home, name='Home'),
]
