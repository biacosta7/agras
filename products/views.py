from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, TypeProduct
from django.contrib import messages
from django.core.exceptions import ValidationError
from seedbeds.models import Seedbed
from django.http import HttpResponse

def product_list_view(request, seedbed_id):
    # Obtém o canteiro com base no ID passado na URL
    seedbed = get_object_or_404(Seedbed, id=seedbed_id)
    
    # Filtra os produtos que pertencem ao canteiro
    queryset = Product.objects.filter(seedbed=seedbed)

    context = {
        'object_list': queryset,
        'seedbed': seedbed  
    }
    return render(request, "product_list.html", context)
 

def product_detail_view(request, id):
	obj = get_object_or_404(Product, id=id)

	context = {
		'object': obj
	} 
	return render(request, "products/product_details.html", context)

def product_update_view(request, seedbed_id, product_id):
    seedbed = get_object_or_404(Seedbed, id=seedbed_id)
    product = get_object_or_404(Product, id=product_id)
    type_products = TypeProduct.objects.all()

    if request.method == "GET":
        return render(request, 'edit_product.html', {
            'product': product,
            'type_products': type_products,
            'seedbed': seedbed  # Passando seedbed no contexto
        })

    else:
        nome = request.POST.get('nome')
        data_plantio = request.POST.get('data_plantio')
        quantidade = request.POST.get('quantidade')

        # Atualizando o produto com a nova informação
        type_product = get_object_or_404(TypeProduct, nome=nome)
        product.nome = type_product
        product.data_plantio = data_plantio
        product.quantidade = quantidade    
        product.save()

        messages.success(request, 'Cultivo editado com sucesso.')

        return redirect('product:product-list', seedbed.id)

def product_delete_view(request, seedbed_id, product_id):
    seedbed = get_object_or_404(Seedbed, id=seedbed_id)
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Produto deletado com sucesso.')
        return redirect('product:product-list', seedbed_id=seedbed.id)
    return render(request, 'delete_product.html', {'product': product, 'seedbed': seedbed})

def create_product_view(request, seedbed_id):
    # Obtém o canteiro correspondente ao ID passado na URL
    seedbed = get_object_or_404(Seedbed, id=seedbed_id)

    # Verifica se a requisição é POST para criar um novo produto
    if request.method == 'POST':
        tipo_nome = request.POST.get('tipo_nome')
        quantidade = request.POST.get('quantidade')
        data_plantio = request.POST.get('data_plantio')

        # Obtém o tipo de produto correspondente ao nome
        tipo_produto = get_object_or_404(TypeProduct, nome=tipo_nome)

        errors = []

        if not tipo_nome:
            errors.append("O campo 'Cultivo' é obrigatório.")
        if not data_plantio:
            errors.append("O campo 'Data de plantio' é obrigatório.")
        if not quantidade:
            errors.append("O campo 'Quantidade' é obrigatório.")
        if errors:
            return render(request, 'create_product.html', {'errors': errors, 'seedbed': seedbed, 'tipos_produtos': tipos_produtos})
        try:
            # Cria um novo produto, associando o seedbed
            product = Product.objects.create(
                nome=tipo_produto,
                quantidade=int(quantidade),
                seedbed=seedbed,  # Associando o produto ao canteiro aqui
                data_plantio=data_plantio
            )
            product.full_clean()  # Validação dos dados
            product.save()  # Salva o produto no banco de dados
            
            messages.success(request, f'Produto {product.nome_type_product} cadastrado com sucesso no canteiro {seedbed.nome}.')

        except ValidationError as e:
            # Tratar erro de validação e retornar mensagens para o usuário
            messages.error(request, f"Erro de validação: {e}")

        return redirect('product:product-list', seedbed.id)  # Redireciona para a lista de produtos

    # Se não for uma requisição POST, renderiza o formulário
    tipos_produtos = TypeProduct.objects.all()  # Obtém todos os tipos de produtos
    return render(request, 'create_product.html', {'seedbed': seedbed, 'tipos_produtos': tipos_produtos})

def create_typeproduct_view(request, seedbed_id):
    # Obtém o canteiro correspondente ao ID passado na URL
    seedbed = get_object_or_404(Seedbed, id=seedbed_id)

    # Verifica se a requisição é POST para criar um novo produto
    if request.method == 'POST':
        nome = request.POST.get('nome').capitalize()
        
        if TypeProduct.objects.filter(nome=nome).exists():
            messages.error(request, f'O cultivo {nome} já existe. Por favor, escolha um nome diferente.')
            return render(request, 'create_typeproduct.html', {'seedbed': seedbed})

        # Cria um novo produto, associando o seedbed
        typeproduct = TypeProduct.objects.create(
            nome=nome
        )

        messages.success(request, f'Novo cultivo {typeproduct.nome} criado com sucesso.')
        return redirect('product:product-list', seedbed.id)  # Redireciona para a lista de produtos

    # Se não for uma requisição POST, renderiza o formulário
    return render(request, 'create_typeproduct.html', {'seedbed': seedbed})