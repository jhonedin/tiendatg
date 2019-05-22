from django.shortcuts import render, redirect, get_object_or_404
from accounts_app.forms import LoginForm
from tienda_app.views import RecomendacionKnn
# Create your views here.

from producto_app.models import ReviewsAmazonDataset # importo el modelo del review del dataset que esta en la BD

def login(request):
	if request.method == 'POST':
		#user = get_object_or_404(ReviewsAmazonDataset, reviewerid = request.POST['reviewerid'], reviewername = request.POST['reviewername'] )
		consulta = ReviewsAmazonDataset.objects.filter(reviewerid = request.POST['reviewerid'],reviewername = request.POST['reviewername'])
		user = consulta[0]
		if user is not None:
			#asinconsultar = 'B00005TQI7'
			asinconsultar = user.asin.asin
			print("asin consultar")
			print(asinconsultar)

			rec = RecomendacionKnn(asinconsultar)
			asinlist = rec[0]
			distanceslist = rec[1]
			return render(request, 'tienda_app/home.html',{'user':user,'asinlist':asinlist,'distanceslist':distanceslist})
			#return render(request, 'tienda_app/home.html',{'user':user})
	else:
		form = LoginForm(request.POST)
	return render(request, 'accounts_app/login.html',{'form':form})
