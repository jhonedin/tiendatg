from django.shortcuts import render, get_object_or_404
# Create your views here.

from producto_app.models import ReviewsAmazonDataset # importo el modelo del review del dataset que esta en la BD

def login(request):
	#user = get_object_or_404(ReviewsAmazonDataset, reviewerid = request.POST['password'], reviewername = request.POST['username'] )
	return render(request, 'accounts_app/login.html',{})


