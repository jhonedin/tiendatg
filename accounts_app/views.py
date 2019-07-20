from django.shortcuts import render, redirect, get_object_or_404
from accounts_app.forms import LoginForm
from accounts_app.forms import RegistroForm
# Create your views here.

from producto_app.models import ReviewsAmazonDataset # importo el modelo del review del dataset que esta en la BD
from producto_app.models import UsuariosNuevos
import psycopg2 # importo la libreria para la conexion a la base de datos
import pandas as pd
import numpy as np

from sqlalchemy import exc
from django.shortcuts import render_to_response

userConsultaGlobal = [] # consulta global del usuario logueado de la tabla de reviews_amazon_dataset
ConsultaGlobal = [] # consulta global de los productos asocioados a un reviewid

def getUserConsultaGlobal():
	userConsultado = userConsultaGlobal
	return userConsultado

def getConsultaGlobal():
	return ConsultaGlobal

def login(request):
	print("Entrando al login")
	if request.method == 'POST':
		#user = get_object_or_404(ReviewsAmazonDataset, reviewerid = request.POST['reviewerid'], reviewername = request.POST['reviewername'] )
		print("Aqui entre en el login despues del post")
		consulta1 = ReviewsAmazonDataset.objects.filter(reviewerid = request.POST['reviewerid'],reviewername = request.POST['reviewername'])
		print("Longitud de los registros de login: "+str(len(consulta1)))
		if consulta1 is not None:
			try:
				elementoIndex = len(consulta1)-1
				if elementoIndex < 0:
					elementoIndex = 0
				user1 = consulta1[elementoIndex]
			except IndexError as e:
				print("Error: "+str(e))
				return render(request, 'accounts_app/errorlogin.html',{})
			global userConsultaGlobal
			userConsultaGlobal = consulta1[0]
			user = user1
			return render(request, 'tienda_app/home.html',{'user':user})
	else:
		form = LoginForm(request.POST)
	return render(request, 'accounts_app/login.html',{'form':form})


def registro(request):
	if request.method == 'POST':
		reviewerID = request.POST['reviewerid']
		reviewerName = request.POST['reviewername']
		asin = 'sinAsin' # cuando es un usuario nuevo no tiene asin aun calificado
		overall = 'sinOverall' # un usuario nuevo aun no ha hecho la calificación de un nuevo producto
		dataNombre = validarNombre(reviewerName)
		if dataNombre.reviewername.get(0)==reviewerName:
			print("Nombre registrado anteriormente")
			return render(request, 'accounts_app/error_registro.html',{})
		#******************************************************
		dataContrasena = validarContrasena(reviewerID)
		if dataNombre.reviewerid.get(0)==reviewerID:
			print("Contrasena registrada anteriormente")
			return render(request, 'accounts_app/error_registro.html',{})
		#******************************************************
		dataVer = validarRegistro(reviewerName,reviewerID)
		print("Nombre verificado")
		print(type(dataVer.reviewername.get(0)))
		print(dataVer.reviewername.get(0))
		print("ID verificado")
		print(type(dataVer.reviewerid.get(0)))
		print(dataVer.reviewerid.get(0))
		if dataVer.reviewername.get(0)==reviewerName and dataVer.reviewerid.get(0)==reviewerID:
			print("Esta registrado anteriormente")
			return render(request, 'accounts_app/error_registro.html',{})
		else:
			print("No estaba registrado anteriormente")
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
			cursor.execute("INSERT into reviews_amazon_dataset(reviewerID,asin,reviewerName,overall) VALUES (%s,%s,%s,%s)",datos)
			conn.commit()
			cursor.close()
			print("Registro exitoso desde registro")
			return render(request, 'accounts_app/confirmacion_registro.html',{})
	else:
		form = RegistroForm(request.POST)
	return render(request, 'accounts_app/registro.html',{'form':form})

def validarRegistro(reviewername,reviewerid):
	try:
		conn = psycopg2.connect("dbname='tienda_bd' user='postgres' host='localhost' password='jhon'")
		print("Conexion a la base de datos exitosa desde validar registro \n")
	except:
		print ("I am unable to connect to the database")
	query = """SELECT * FROM reviews_amazon_dataset r  WHERE reviewerid='"""+reviewerid+"""'"""+""" AND """+""" reviewername='"""+reviewername+"""'"""
	data_query = pd.read_sql(query, conn)
	return data_query

def validarNombre(reviewername):
	try:
		conn = psycopg2.connect("dbname='tienda_bd' user='postgres' host='localhost' password='jhon'")
		print("Conexion a la base de datos exitosa desde validar nombre \n")
	except:
		print ("I am unable to connect to the database")
	query = """SELECT * FROM reviews_amazon_dataset r  WHERE reviewername='"""+reviewername+"""'"""
	data_query = pd.read_sql(query, conn)
	return data_query

def validarContrasena(reviewerid):
	try:
		conn = psycopg2.connect("dbname='tienda_bd' user='postgres' host='localhost' password='jhon'")
		print("Conexion a la base de datos exitosa desde validar nombre \n")
	except:
		print ("I am unable to connect to the database")
	query = """SELECT * FROM reviews_amazon_dataset r  WHERE reviewerid='"""+reviewerid+"""'"""
	data_query = pd.read_sql(query, conn)
	return data_query
