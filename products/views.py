from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import RegisterProductForm

def product_list_view(request):
	queryset = Product.objects.all() #list of objects
	
	context = {
		'object_list': queryset
	} 
	
	return render(request, "products/product_list.html", context) 

def product_detail_view(request, id):
	obj = get_object_or_404(Product, id=id)

	context = {
		'object': obj
	} 
	return render(request, "products/product_details.html", context)

def product_register_view(request):
	if request.method == 'POST':
		form = RegisterProductForm(request.POST)
		if form.is_valid():
			product = form.save(commit=False)
			product.author_user = request.user
			product.save()
			return redirect('products:product-list')
	else:
		form = RegisterProductForm()
	return render(request, 'products/product_register.html', {'form': form})
