from django.urls import path, include
from . import views

urlpatterns = [
    path('Tienda/', views.Tienda, name='Tienda'),
    path('Recomendacion/', views.RecomendacionKnn, name='RecomendacionKnn'),
]

