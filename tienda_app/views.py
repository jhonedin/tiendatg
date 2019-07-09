from producto_app.views import Getproducto_asin
from django.shortcuts import render, redirect, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from producto_app.models import ReviewsAmazonDataset
from producto_app.models import MetadataAmazonDataset
from accounts_app.views import getUserConsultaGlobal
# Librerias del sistema de recomendación
import pandas as pd
import numpy as np
import psycopg2
import time
import warnings
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import TruncatedSVD

# Create your views here.
asinlistGlobal = []
distanceslistGlobal = []
finalTimeGlobal = 0

asinlistGlobalSVD = []
distanceslistGlobalSVD = []
finalTimeGlobalSVD = 0

def Home(request):
	user = getUserConsultaGlobal()
	asinlist = asinlistGlobal
	ObjProducto1 = buscarProductoxAsin(asinlist[0])
	ObjProducto2 = buscarProductoxAsin(asinlist[1])
	ObjProducto3 = buscarProductoxAsin(asinlist[2])
	ObjProducto4 = buscarProductoxAsin(asinlist[3])
	ObjProducto5 = buscarProductoxAsin(asinlist[4])

	return render(request, 'tienda_app/home.html',{'user':user,
	'ObjProducto1':ObjProducto1,
	'ObjProducto2':ObjProducto2,
	'ObjProducto3':ObjProducto3,
	'ObjProducto4':ObjProducto4,
	'ObjProducto5':ObjProducto5})

# Función encargarda de renderizar la recomendación mediante el algoritmo KNN
def vistaRecomendacionKnn(request):
	user = getUserConsultaGlobal()
	if user.asin.asin == 'sinAsin':
		print("No hay recomendaciones que mostrar")
		ObjProducto1 = None
		ObjProducto2 = None
		ObjProducto3 = None
		ObjProducto4 = None
		ObjProducto5 = None
		ObjProducto6 = None
		ObjProducto7 = None
		ObjProducto8 = None
		ObjProducto9 = None
		ObjProducto10 = None
		return render(request, 'tienda_app/knn.html',{'user':user,
		'ObjProducto1':ObjProducto1,
		'ObjProducto2':ObjProducto2,
		'ObjProducto3':ObjProducto3,
		'ObjProducto4':ObjProducto4,
		'ObjProducto5':ObjProducto5,
		'ObjProducto6':ObjProducto6,
		'ObjProducto7':ObjProducto7,
		'ObjProducto8':ObjProducto8,
		'ObjProducto9':ObjProducto9,
		'ObjProducto10':ObjProducto10})
	else:
		# Del review se extrae el usuario, y el asin (id producto) asociado a ese review de compra
	 	# con respecto al cual se realizara la recomendacion
		asinconsultar = user.asin.asin
		print("objeto asin consultar")
		print("ID:"+" "+user.asin.asin)
		print("Precio:"+" "+user.asin.price)
		print("Descripcion:"+" "+user.asin.description)
		print("Marca:"+" "+user.asin.brand)
		print("Categorias:"+" "+user.asin.categories)
		rec = RecomendacionKnn(asinconsultar) # rec contiene rec=[[lista_id_productos],[lista_distanciasknn_productos]]
		asinlist = rec[0] # extrae los id de los productos recomendados
		distanceslist = rec[1] # extrae las distancias knn de los productos recomendados
		# Se espera que en knn se recomiende maximo 10 productos, aunque la cantidad de productos que se recomienden
		# dependera de ajustar el parametro n_neighbors, en la función RecomendacionKnn
		ObjProducto1 = None
		ObjProducto2 = None
		ObjProducto3 = None
		ObjProducto4 = None
		ObjProducto5 = None
		ObjProducto6 = None
		ObjProducto7 = None
		ObjProducto8 = None
		ObjProducto9 = None
		ObjProducto10 = None
		for i in range(0,len(asinlist)):
			if(i==0):
				ObjProducto1 = buscarProductoxAsin(asinlist[i])
			if(i==1):
				ObjProducto2 = buscarProductoxAsin(asinlist[i])
			if(i==2):
				ObjProducto3 = buscarProductoxAsin(asinlist[i])
			if(i==3):
				ObjProducto4 = buscarProductoxAsin(asinlist[i])
			if(i==4):
				ObjProducto5 = buscarProductoxAsin(asinlist[i])
			if(i==5):
				ObjProducto6 = buscarProductoxAsin(asinlist[i])
			if(i==6):
				ObjProducto7 = buscarProductoxAsin(asinlist[i])
			if(i==7):
				ObjProducto8 = buscarProductoxAsin(asinlist[i])
			if(i==8):
				ObjProducto9 = buscarProductoxAsin(asinlist[i])
			if(i==9):
				ObjProducto10 = buscarProductoxAsin(asinlist[i])
		return render(request, 'tienda_app/knn.html',{'user':user,
		'ObjProducto1':ObjProducto1,
		'ObjProducto2':ObjProducto2,
		'ObjProducto3':ObjProducto3,
		'ObjProducto4':ObjProducto4,
		'ObjProducto5':ObjProducto5,
		'ObjProducto6':ObjProducto6,
		'ObjProducto7':ObjProducto7,
		'ObjProducto8':ObjProducto8,
		'ObjProducto9':ObjProducto9,
		'ObjProducto10':ObjProducto10})

# Función encargarda de renderizar la recomendación mediante el algoritmo SVM
def vistaRecomendacionSvd(request):
	user = getUserConsultaGlobal()
	if user.asin.asin == 'sinAsin':
		print("No hay recomendaciones que mostrar")
		ObjProducto1 = None
		ObjProducto2 = None
		ObjProducto3 = None
		ObjProducto4 = None
		ObjProducto5 = None
		ObjProducto6 = None
		ObjProducto7 = None
		ObjProducto8 = None
		ObjProducto9 = None
		ObjProducto10 = None
		return render(request, 'tienda_app/svd.html',{'user':user,
		'ObjProducto1':ObjProducto1,
		'ObjProducto2':ObjProducto2,
		'ObjProducto3':ObjProducto3,
		'ObjProducto4':ObjProducto4,
		'ObjProducto5':ObjProducto5,
		'ObjProducto6':ObjProducto6,
		'ObjProducto7':ObjProducto7,
		'ObjProducto8':ObjProducto8,
		'ObjProducto9':ObjProducto9,
		'ObjProducto10':ObjProducto10})
	else:
		asinconsultar = user.asin.asin
		print("objeto asin consultar")
		print("ID:"+" "+user.asin.asin)
		print("Precio:"+" "+user.asin.price)
		print("Descripcion:"+" "+user.asin.description)
		print("Marca:"+" "+user.asin.brand)
		print("Categorias:"+" "+user.asin.categories)
		asinlist= []
		rec_svd = recomendacionColaborativaSVD(asinconsultar)
		for i in range(0,len(rec_svd)):
			tupla = rec_svd[i]
			asinlist.append(tupla[0])
		ObjProducto1 = None
		ObjProducto2 = None
		ObjProducto3 = None
		ObjProducto4 = None
		ObjProducto5 = None
		ObjProducto6 = None
		ObjProducto7 = None
		ObjProducto8 = None
		ObjProducto9 = None
		ObjProducto10 = None
		for i in range(0,len(asinlist)):
			if(i==0):
				ObjProducto1 = buscarProductoxAsin(asinlist[i])
			if(i==1):
				ObjProducto2 = buscarProductoxAsin(asinlist[i])
			if(i==2):
				ObjProducto3 = buscarProductoxAsin(asinlist[i])
			if(i==3):
				ObjProducto4 = buscarProductoxAsin(asinlist[i])
			if(i==4):
				ObjProducto5 = buscarProductoxAsin(asinlist[i])
			if(i==5):
				ObjProducto6 = buscarProductoxAsin(asinlist[i])
			if(i==6):
				ObjProducto7 = buscarProductoxAsin(asinlist[i])
			if(i==7):
				ObjProducto8 = buscarProductoxAsin(asinlist[i])
			if(i==8):
				ObjProducto9 = buscarProductoxAsin(asinlist[i])
			if(i==9):
				ObjProducto10 = buscarProductoxAsin(asinlist[i])
		return render(request, 'tienda_app/svd.html',{'user':user,
		'ObjProducto1':ObjProducto1,
		'ObjProducto2':ObjProducto2,
		'ObjProducto3':ObjProducto3,
		'ObjProducto4':ObjProducto4,
		'ObjProducto5':ObjProducto5,
		'ObjProducto6':ObjProducto6,
		'ObjProducto7':ObjProducto7,
		'ObjProducto8':ObjProducto8,
		'ObjProducto9':ObjProducto9,
		'ObjProducto10':ObjProducto10})


def metricas(request):
	# Variables metricas algoritmo knn
	asinlist = asinlistGlobal
	distanceslist = distanceslistGlobal
	finalTimeRec = finalTimeGlobal
	######
	# Variables metricas algoritmo svd
	asinlistsvd = asinlistGlobalSVD
	distanceslistsvd = distanceslistGlobalSVD
	finalTimesvd = finalTimeGlobalSVD
	return render(request, 'tienda_app/metricas.html',{
	'asinlist':asinlist,
	'distanceslist':distanceslist,
	'finalTimeRec':finalTimeRec,
	'asinlistsvd':asinlistsvd,
	'distanceslistsvd':distanceslistsvd,
	'finalTimesvd':finalTimesvd
	})

# Función encargada de buscar un producto por su id en este caso el asin del producto
# Entrada: un String que tiene el identificador unico del producto o su asin
# Salida: Un objeto del producto del asin correspondiente
def buscarProductoxAsin(asin):
	objProducto = MetadataAmazonDataset.objects.filter(asin=str(asin))
	return objProducto

# Función encargada de renderizar la galeria de productos
def galeriaProducto(request):
	try:
		conn = psycopg2.connect("dbname='tienda_bd' user='postgres' host='localhost' password='jhon'")
		print("Conexion a la base de datos exitosa \n")
	except:
		print ("I am unable to connect to the database")
	query = """SELECT * FROM metadata_amazon_dataset m  WHERE m.price !='0.00' AND m.description !='Sin descripcion' AND m.description !='' AND m.brand != 'Sin marca' """
	data_query = pd.read_sql(query, conn)
	print("data_query")
	print(data_query)
	listaIDFiltrados = list(data_query.loc[0:,'asin'].values)
	listaTitleFiltrados = list(data_query.loc[0:,'title'].values)
	listaUrlImagFiltrados = list(data_query.loc[0:,'imurl'].values)
	listaPriceFiltrados = list(data_query.loc[0:,'price'].values)
	listaDescriptionFiltrados = list(data_query.loc[0:,'description'].values)
	listaBrandFiltrados = list(data_query.loc[0:,'brand'].values)
	listaCategoriesFiltrados = list(data_query.loc[0:,'categories'].values)
	objGaleriaList = []
	for i in range(0,10):
		auxList = [listaIDFiltrados[i],
				  listaTitleFiltrados[i],
				  listaUrlImagFiltrados[i],
				  listaPriceFiltrados[i],
				  listaDescriptionFiltrados[i],
				  listaBrandFiltrados[i],
				  listaCategoriesFiltrados[i]]
		objGaleriaList.append(auxList)
	return render(request, 'tienda_app/galeria.html',{'objGaleriaList':objGaleriaList})


def RecomendacionKnn(asinconsultar):
	try:
		conn = psycopg2.connect("dbname='tienda_bd' user='postgres' host='localhost' password='jhon'")
		print("Conexion a la base de datos exitosa \n")
	except:
		print ("I am unable to connect to the database")
	query1 = """ SELECT r.reviewerid, m.asin, r.overall FROM metadata_amazon_dataset m JOIN reviews_amazon_dataset r ON m.asin = r.asin WHERE m.price !='0.00' AND r.overall !='1.0' AND r.overall !='2.0' AND m.description !='Sin descripcion' AND m.description !='''' AND m.brand != 'Sin marca' """
	data_query = pd.read_sql(query1, conn)
	startTime = time.time()
	print("IMPLEMENTACION RECOMENDACION KNN")
	print("\n")
	cuenta_rating_producto = (data_query.groupby(by = ['asin'])['overall'].count().reset_index().rename(columns={'overall': 'cuentaTotalRatings'})[['asin','cuentaTotalRatings']])
	totales_ratings = data_query.merge(cuenta_rating_producto, left_on = 'asin', right_on = 'asin', how = 'left')
	ratings_minimo = 100
	productos_mas_populares = totales_ratings.query('cuentaTotalRatings >= @ratings_minimo')
	ratings_pivot = productos_mas_populares.pivot(index = 'asin', columns = 'reviewerid', values = 'overall').fillna(0)
	ratings_matrix_sparse = csr_matrix(ratings_pivot.values.astype(float))
	model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
	model_knn.fit(ratings_matrix_sparse)
	reviewerid_matriz_productos = ratings_pivot.index
	lista_reviewerid_productos = list(reviewerid_matriz_productos)
	ind_producto_target = lista_reviewerid_productos.index(asinconsultar) # 'B00005TQI7'
	query_index = ind_producto_target
	distances, indices = model_knn.kneighbors(ratings_pivot.iloc[query_index, :].values.reshape(1, -1), n_neighbors = 6) # con values corregi el error de AttributeError: 'Series' object has no attribute 'reshape'
	#rec =  distances, indices
	asinlist = []
	distanceslist = []
	for i in range(0, len(distances.flatten())):
		if i == 0:
			print ('Recommendations for {0}:\n'.format(ratings_pivot.index[query_index]))
		else:
			#print ('{0}: {1}, with distance of {2}:'.format(i, ratings_pivot.index[indices.flatten()[i]], distances.flatten()[i]))
			if(distances.flatten()[i] < 1):
				asinlist.append(ratings_pivot.index[indices.flatten()[i]])
				distanceslist.append(distances.flatten()[i])
	rec = asinlist, distanceslist
	global asinlistGlobal
	global distanceslistGlobal
	global finalTimeGlobal
	asinlistGlobal = asinlist
	distanceslistGlobal = distanceslist
	finalTime = time.time() - startTime
	finalTimeGlobal = finalTime
	print ('El script tomó {0} segundos'.format(finalTime))
	return rec


def recomendacionColaborativaSVD(asinconsultar):
	try:
		conn = psycopg2.connect("dbname='tienda_bd' user='postgres' host='localhost' password='jhon'")
		print("Conexion a la base de datos exitosa \n")
	except:
		print ("I am unable to connect to the database")

	query2 = """ SELECT r.reviewerid, m.asin, r.overall FROM metadata_amazon_dataset m JOIN reviews_amazon_dataset r ON m.asin = r.asin WHERE m.price !='0.00' AND r.overall !='1.0' AND r.overall !='2.0' AND m.description !='Sin descripcion' AND m.description !='''' AND m.brand != 'Sin marca' """
	data_query = pd.read_sql(query2, conn)
	startTime = time.time()
	print("IMPLEMENTACION RECOMENDACION COLABORATIVA SVD")
	print("\n")
	cuenta_rating_producto = (data_query.groupby(by = ['asin'])['overall'].count().reset_index().rename(columns={'overall': 'cuentaTotalRatings'})[['asin','cuentaTotalRatings']])
	totales_ratings = data_query.merge(cuenta_rating_producto, left_on = 'asin', right_on = 'asin', how = 'left')
	ratings_minimo = 100
	productos_mas_populares = totales_ratings.query('cuentaTotalRatings >= @ratings_minimo')
	ratings_pivot = productos_mas_populares.pivot(index = 'asin', columns = 'reviewerid', values = 'overall').fillna(0)
	X = ratings_pivot.values
	SVD = TruncatedSVD(n_components=20, random_state=22, n_iter=10)
	matriz_svd = SVD.fit_transform(X)
	warnings.filterwarnings("ignore",category =RuntimeWarning)
	matriz_corr = np.corrcoef(matriz_svd)
	asin_matriz_productos = ratings_pivot.index
	lista_asin_productos = list(asin_matriz_productos)
	rec_svd=[]
	asin_producto = asinconsultar
	ind_producto_target = lista_asin_productos.index(asin_producto)
	lista_producto_corr_target = list(matriz_corr[ind_producto_target]) #calificaciones de productos respecto a target
	max_indices=[]
	prueba=[]
	for i in lista_producto_corr_target:
		if (i<1.0) & (i>0.8):
			max_ind= lista_producto_corr_target.index(i)
			max_indices.append(max_ind)
			asin_ind = asin_matriz_productos[max_ind]
			prueba.append([asin_ind,i])
	rec_svd= sorted(prueba, key=lambda x:x[0], reverse=True)[1:10]
	global asinlistGlobalSVD
	global distanceslistGlobalSVD
	global finalTimeGlobalSVD
	asin = []
	distances = []
	for i in range(0,len(rec_svd)):
		tupla = rec_svd[i]
		asin.append(tupla[0])
		distances.append(tupla[1])
	asinlistGlobalSVD = asin
	distanceslistGlobalSVD = distances
	finalTime = time.time() - startTime
	finalTimeGlobalSVD = finalTime
	print ('El script tomó {0} segundos'.format(finalTime))
	return rec_svd

def calificarBtnUno(request):
	return render(request, 'tienda_app/galeria.html',{}) 
