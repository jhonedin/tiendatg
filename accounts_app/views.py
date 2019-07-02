from django.shortcuts import render, redirect, get_object_or_404
from accounts_app.forms import LoginForm
from accounts_app.forms import RegistroForm
# Create your views here.

from producto_app.models import ReviewsAmazonDataset # importo el modelo del review del dataset que esta en la BD

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
	
	return render(request, 'accounts_app/registro.html',{})
