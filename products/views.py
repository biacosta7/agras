from django.shortcuts import render, redirect
from .models import Product

def product_list_view(request):
	queryset = Product.objects.all() #list of objects
	
	context = {
		'object_list': queryset
	} 
	
	return render(request, "products/product_list.html", context) 

def product_detail_view(request):
	obj = Product.object.get(id=1)

	context = {
		'object': obj
	}
	return render(request, "product/detail.html", context)