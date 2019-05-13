from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.Home, name='Home'),
    path('recomendacion/', views.RecomendacionKnn, name='RecomendacionKnn'),
]

