from django.urls import path
#from apps.usuario.views import SignUpView
from apps.partido import views

urlpatterns = [
	"""
 	path('JugadosEspaña', views.JuegosJugadosLigaEspaña, name='JuegosJugadosLigaEspaña'),
 	path('JugadosInglaterra', views.JuegosJugadosLigaInglesa, name='JuegosJugadosLigaInglesa'),
 	path('JugadosItalia', views.JuegosJugadosLigaItaliana, name='JuegosJugadosLigaItaliana'),
 	path('JugadosAlemania', views.JuegosJugadosLigaAlemana, name='JuegosJugadosLigaAlemana'),
 	path('ProgramadosEspaña', views.JuegosProgramadosLigaEspaña, name='JuegosProgramadosLigaEspaña'),
 	path('ProgramadosInglaterra', views.JuegosProgramadosLigaInglesa, name='JuegosProgramadosLigaInglesa'),
 	path('ProgramadosItalia', views.JuegosProgramadosLigaItaliana, name='JuegosProgramadosLigaItaliana'),
 	path('ProgramadosAlemania', views.JuegosProgramadosLigaAlemana, name='JuegosProgramadosLigaAlemana'),
 	path('JugadosTodasLigas', views.JugadosTodasLasLigas, name='JugadosTodasLasLigas'),
    #path('signup/', SignUpView.as_view(), name="signup"),
    """
]
