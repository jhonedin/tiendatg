from django.shortcuts import render, get_object_or_404
from producto_app.views import Getproducto_asin

from django.shortcuts import render, redirect, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from producto_app.models import ReviewsAmazonDataset
from producto_app.models import MetadataAmazonDataset
# Librerias del sistema de recomendación
import pandas as pd
import numpy as np
import psycopg2
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

# Create your views here.
asinlistGlobal = []
distanceslistGlobal = []

def Home(request,asin):
	asinconsultar = asin
	objListaDeProductos = RecomendacionKnn(asinconsultar)
	return render(request, 'tienda_app/home.html',{'objListaDeProductos':objListaDeProductos})
	#rec = RecomendacionKnn(asinconsultar)
	#asinlist = rec[0]
	#distanceslist = rec[1]
	#return render(request, 'tienda_app/home.html',{'asinlist':asinlist,'distanceslist':distanceslist})

def metricas(request):
	asinlist = asinlistGlobal
	distanceslist = distanceslistGlobal
	return render(request, 'tienda_app/metricas.html',{'asinlist':asinlist,'distanceslist':distanceslist})

# Función encargada de buscar un producto por su id en este caso el asin del producto
# Entrada: un String que tiene el identificador unico del producto o su asin
# Salida: Un objeto del producto del asin correspondiente
def buscarProductoxAsin(asin):
	objProducto = MetadataAmazonDataset.objects.filter(asin=str(asin))
	return objProducto

def RecomendacionKnn(asinconsultar):
	try:
		conn = psycopg2.connect("dbname='tienda_bd' user='postgres' host='localhost' password='jhon'")
		print("Conexion a la base de datos exitosa \n")
	except:
		print ("I am unable to connect to the database")
	query1 = """ SELECT r.reviewerid, m.asin, r.overall FROM metadata_amazon_dataset m JOIN reviews_amazon_dataset r ON m.asin = r.asin WHERE m.price !='0.00' AND r.overall !='1.0' AND r.overall !='2.0' AND m.description !='Sin descripcion' AND m.description !='''' AND m.brand != 'Sin marca' """
	data_query = pd.read_sql(query1, conn)
	print("IMPLEMENTACION RECOMENDACION")
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
			asinlist.append(ratings_pivot.index[indices.flatten()[i]])
			distanceslist.append(distances.flatten()[i])
	rec = asinlist, distanceslist
	global asinlistGlobal
	global distanceslistGlobal
	asinlistGlobal = asinlist
	distanceslistGlobal = distanceslist
	return rec
