from django.shortcuts import render, redirect, get_object_or_404
from accounts_app.forms import LoginForm
from accounts_app.forms import RegistroForm
# Create your views here.

from producto_app.models import ReviewsAmazonDataset # importo el modelo del review del dataset que esta en la BD
from producto_app.models import UsuariosNuevos
import psycopg2 # importo la libreria para la conexion a la base de datos

userConsultaGlobal = [] # consulta global del usuario logueado de la tabla de reviews_amazon_dataset
userConsultaGlobalNewUser = [] # consulta global del usuario logueado de la tabla usuarios_nuevos

def getUserConsultaGlobal():
	userConsultado = userConsultaGlobal
	return userConsultado

def getUserConsultaGlobalNewUser():
	newUserConsultado = getUserConsultaGlobalNewUser
	return newUserConsultado

def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		return render(request, 'accounts_app/login.html',{'form':form})
	else:
		form = LoginForm(request.POST)
	return render(request, 'accounts_app/login.html',{'form':form})

"""
def login(request):
	if request.method == 'POST':
		#user = get_object_or_404(ReviewsAmazonDataset, reviewerid = request.POST['reviewerid'], reviewername = request.POST['reviewername'] )
		consulta1 = ReviewsAmazonDataset.objects.filter(reviewerid = request.POST['reviewerid'],reviewername = request.POST['reviewername'])
		consulta2 = UsuariosNuevos.objects.filter(reviewerid = request.POST['reviewerid'],reviewername = request.POST['reviewername'])
		if consulta1 is not None:
			user1 = consulta1[0]
			global userConsultaGlobal
			userConsultaGlobal = consulta1[0]
			user = user1
			return render(request, 'tienda_app/home.html',{'user':user})
		if consulta2 is not None:
			user2 = consulta2[0]
			global userConsultaGlobalNewUser
			userConsultaGlobalNewUser = consulta2[0]
			user = user2
			return render(request, 'tienda_app/home.html',{'user':user})
	else:
		form = LoginForm(request.POST)

	return render(request, 'accounts_app/login.html',{'form':form})
"""

def registro(request):
	if request.method == 'POST':
		reviewerID = request.POST['reviewerid']
		reviewerName = request.POST['reviewername']
		datos = []
		datos.append(reviewerID)
		datos.append(reviewerName)
		try:
			conn = psycopg2.connect("dbname='tienda_bd' user='postgres' host='localhost' password='jhon'")
			print("Conexion a la base de datos exitosa desde registro \n")
		except:
			print ("I am unable to connect to the database desde registro")
		cursor = conn.cursor()
		cursor.execute("INSERT into usuarios_nuevos(reviewerID,reviewerName) VALUES (%s, %s)",datos)
		conn.commit()
		cursor.close()
		print("Registro exitoso desde registro")
		form = LoginForm(request.POST)
		return render(request, 'accounts_app/login.html',{'form':form})
	else:
		form = RegistroForm(request.POST)
	return render(request, 'accounts_app/registro.html',{'form':form})
