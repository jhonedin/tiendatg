from django.shortcuts import render
from producto_app.views import Getproducto_asin

# Librerias del sistema de recomendación 
import pandas as pd
import numpy as np
import psycopg2
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

# Create your views here.

def Home(request):
	return render(request, 'home.html',{})


def Tienda(request):
	#asinconsultar = '1028907516'
	#producto = Getproducto_asin(asinconsultar)
	rec = RecomendacionKnn()
	asinlist = rec[0]
	distanceslist = rec[1]
	return render(request, 'tienda.html',{'asinlist':asinlist,'distanceslist':distanceslist}) 
	#return render(request, 'tienda.html',{'producto':producto})


def RecomendacionKnn():
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
	ind_producto_target = lista_reviewerid_productos.index('B00005TQI7')
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
	return rec
	#return render(request, 'tienda.html',{'asinlist':asinlist,'distanceslist':distanceslist}) 