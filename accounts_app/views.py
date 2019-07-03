from django.shortcuts import render, redirect, get_object_or_404
from accounts_app.forms import LoginForm
from accounts_app.forms import RegistroForm
# Create your views here.

from producto_app.models import ReviewsAmazonDataset # importo el modelo del review del dataset que esta en la BD
import psycopg2 # importo la libreria para la conexion a la base de datos

userConsultaGlobal = []

def getUserConsultaGlobal():
	userConsultado = userConsultaGlobal
	return userConsultado

def login(request):
	if request.method == 'POST':
		#user = get_object_or_404(ReviewsAmazonDataset, reviewerid = request.POST['reviewerid'], reviewername = request.POST['reviewername'] )
		consulta = ReviewsAmazonDataset.objects.filter(reviewerid = request.POST['reviewerid'],reviewername = request.POST['reviewername'])
		user = consulta[0]
		if user is not None:
			global userConsultaGlobal
			userConsultaGlobal = consulta[0]
			return render(request, 'tienda_app/home.html',{'user':user})
	else:
		form = LoginForm(request.POST)

	return render(request, 'accounts_app/login.html',{'form':form})

def registro(request):
	if request.method == 'POST':
		reviewerName = request.POST['reviewername']
		reviewerID = request.POST['reviewerid']
		asin = '-1'
		overall = '-1'
		datos = []
		datos.append(reviewerID)
		datos.append(asin)
		datos.append(reviewerName)
		datos.append(overall)
		try:
			conn = psycopg2.connect("dbname='tienda_bd' user='postgres' host='localhost' password='jhon'")
			print("Conexion a la base de datos exitosa desde registro \n")
		except:
			print ("I am unable to connect to the database desde registro")
		cursor = conn.cursor()
		cursor.execute("INSERT into reviews_amazon_dataset(reviewerID,asin,reviewerName,overall) VALUES (%s, %s,%s,%s)",datos)
		conn.commit()
		cursor.close()
		print("Registro exitoso desde registro")
		form = LoginForm(request.POST)
		return render(request, 'accounts_app/login.html',{'form':form})
	else:
		form = RegistroForm(request.POST)
	return render(request, 'accounts_app/registro.html',{'form':form})
