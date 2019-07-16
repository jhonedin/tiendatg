"""tiendaweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tienda_app.views import metricas
from tienda_app.views import galeriaProducto
from tienda_app.views import Home
from tienda_app.views import vistaRecomendacionKnn
from tienda_app.views import vistaRecomendacionSvd
from tienda_app.views import calificarBtnUno
from tienda_app.views import calificarBtnDos
from tienda_app.views import calificarBtnTres
from tienda_app.views import calificarBtnCuatro
from tienda_app.views import calificarBtnCinco
from accounts_app.views import login
from accounts_app.views import registro

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login, name='login'),
    path('tienda_app/', include('tienda_app.urls')),
    path('accounts_app/', include('accounts_app.urls')),
    path('login/',login, name='login'),
    path('registro/',registro, name='registro'),
    path('calificarBtnUno/(?P<asin>[-\w]+)(?P<nombreUser>[-\w]+)(?P<idUser>[-\w]+)',calificarBtnUno, name='calificarBtnUno'),
    path('calificarBtnDos/(?P<asin>[-\w]+)(?P<nombreUser>[-\w]+)(?P<idUser>[-\w]+)',calificarBtnDos, name='calificarBtnDos'),
    path('calificarBtnTres/(?P<asin>[-\w]+)(?P<nombreUser>[-\w]+)(?P<idUser>[-\w]+)',calificarBtnTres, name='calificarBtnTres'),
    path('calificarBtnCuatro/(?P<asin>[-\w]+)(?P<nombreUser>[-\w]+)(?P<idUser>[-\w]+)',calificarBtnCuatro, name='calificarBtnCuatro'),
    path('calificarBtnCinco/(?P<asin>[-\w]+)(?P<nombreUser>[-\w]+)(?P<idUser>[-\w]+)',calificarBtnCinco, name='calificarBtnCinco'),
    path('Home/',Home, name='Home'),
    path('metricas/',metricas, name='metricas'),
    path('galeriaProducto/',galeriaProducto, name='galeriaProducto'),
    path('vistaRecomendacionKnn/',vistaRecomendacionKnn, name='vistaRecomendacionKnn'),
    path('vistaRecomendacionSvd/',vistaRecomendacionSvd, name='vistaRecomendacionSvd'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
