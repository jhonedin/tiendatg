from django.shortcuts import render
from .models import MetadataAmazonDataset

# Create your views here.

def Getproducto_asin(asin):
	producto = MetadataAmazonDataset.objects.filter(pk=asin)
	return producto 
	#return render(request, 'partido/partido.html',{'partidos':partidos})

