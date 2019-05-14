from django.shortcuts import render, redirect, get_object_or_404
from accounts_app.forms import LoginForm
# Create your views here.

from producto_app.models import ReviewsAmazonDataset # importo el modelo del review del dataset que esta en la BD

def login(request):
	if request.method == 'POST':
		user = get_object_or_404(ReviewsAmazonDataset, reviewerid = request.POST['reviewerid'], reviewername = request.POST['reviewername'] )
		if user is not None:
			return render(request, 'tienda_app/home.html',{'user':user})
	else:
		form = LoginForm(request.POST)
	return render(request, 'accounts_app/login.html',{'form':form})
