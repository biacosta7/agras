from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, TypeProduct
from .forms import RegisterProductForm
from django.contrib import messages
from django.core.exceptions import ValidationError

def add_product(request):
    if request.method == "GET":
        # Renderiza a página com o formulário vazio
        return render(request, 'create_product.html')

    elif request.method == "POST":
        nome = request.POST.get('nome')
        data_plantio = request.POST.get('data_plantio')
        quantidade = request.POST.get('quantidade')

        errors = []

        if not nome:
            errors.append("O campo 'Nome' é obrigatório.")
        if not data_plantio:
            errors.append("O campo 'Data de plantio' é obrigatório.")
        if not quantidade:
            errors.append("O campo 'Quantidade' é obrigatório.")
        if errors:
            return render(request, 'create_product.html', {'errors': errors})
        try:
            # Criação do produto no banco de dados
            product = Product(
                nome=nome,
                data_plantio=data_plantio,
                quantidade=quantidade
            )
            product.full_clean()  # Validação dos dados
            product.save()  # Salva o produto no banco de dados
            
            # Redireciona para a página de sucesso após a criação
            return redirect('some_success_url')

        except ValidationError as e:
            # Tratar erro de validação e retornar mensagens para o usuário
            messages.error(request, f"Erro de validação: {e}")
    
    return render(request, 'create_product.html')  # Renderiza a página novamente se houver erro

def product_list_view(request):
	queryset = Product.objects.all()
	
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

def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "GET":
        return render(request, 'edit_product.html', {'product': product})
    else:
        name = request.POST.get('name')
        data_plantio = request.POST.get('data_plantio')
        quantidade = request.POST.get('quantidade')

        valid_char = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        if not set(name).issubset(valid_char):
            messages.error(request, 'O nome do produto deve conter apenas letras, números ou underlines, sem espaços ou caracteres especiais.')
            return redirect('/')
		
        product.name = name
        product.data_plantio = data_plantio
        product.quantidade = quantidade    
        product.save()
        messages.success(request, 'Produto editado com sucesso.')

        return redirect('products:product-list')

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Produto deletado com sucesso.')
    return redirect('get_all_users')

def create_type_product(request):
    if request.method == "GET":
        return render(request, 'create_type_product.html')  # Renderiza o template para cadastro

    elif request.method == "POST":
        nome = request.POST.get('nome')  # Captura o valor do campo 'nome' do formulário

        if nome:  # Validação simples para garantir que o nome não está vazio
            TypeProduct.objects.create(nome=nome)  # Cria o objeto e salva no banco de dados
            return redirect('some_success_url')  # Redireciona após o sucesso

        # Se o nome estiver vazio, renderiza o formulário novamente com uma mensagem de erro
        return render(request, 'create_type_product.html', {'error': 'Nome não pode estar vazio'})

    return render(request, 'create_type_product.html')