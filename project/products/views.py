from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, TypeProduct
from django.contrib import messages
from django.core.exceptions import ValidationError
from communities.models import Community
from seedbeds.models import Seedbed

@login_required  
def create_product_view(request, seedbed_id, community_id):
    community = get_object_or_404(Community, id=community_id)
    seedbed = get_object_or_404(Seedbed, id=seedbed_id)

    if request.method == 'POST':
        type_name = request.POST.get('tipo_nome')
        quantity = request.POST.get('quantidade')
        planting_date = request.POST.get('data_plantio')

        # Verificando se o tipo de produto existe na comunidade correta
        type_product = get_object_or_404(TypeProduct, name=type_name, community=community)

        errors = []

        # Validação dos campos
        if not type_name:
            errors.append("O campo 'Cultivo' é obrigatório.")
        if not planting_date:
            errors.append("O campo 'Data de plantio' é obrigatório.")
        if not quantity:
            errors.append("O campo 'Quantidade' é obrigatório.")
        
        if errors:
            return render(request, 'create_product.html', {
                'errors': errors,
                'community': community,
                'tipos_produtos': TypeProduct.objects.filter(community=community)  # Filtrando por comunidade
            })

        try:
            # Criando o produto associado à comunidade
            product = Product.objects.create(
                type_product=type_product,
                seedbed=seedbed, 
                community=community,
                quantity=int(quantity),
                planting_date=planting_date
            )
            product.full_clean()  
            product.save()
            
            messages.success(request, f'Produto {product.nome_type_product} cadastrado com sucesso no canteiro {seedbed.nome}.')

        except ValidationError as e:
            messages.error(request, f"Erro de validação: {e}")

        return redirect('dashboard', community.id)
    
    context={
        'community': community, 
        'tipos_produtos': tipos_produtos,
        'seedbed': seedbed,
    }

    # Filtrando tipos de produtos por comunidade
    tipos_produtos = TypeProduct.objects.filter(community=community)
    return render(request, 'create_product.html', context)

@login_required  
def create_typeproduct_view(request, community_id):
    community = get_object_or_404(Community, id=community_id)

    if request.method == 'POST':
        nome = request.POST.get('nome').capitalize()
        
        # Verificando se o tipo de produto já existe na mesma comunidade
        if TypeProduct.objects.filter(name=nome, community=community).exists():
            messages.error(request, f'O cultivo {nome} já existe na comunidade {community.name}. Por favor, escolha um nome diferente.')
            return render(request, 'create_typeproduct.html', {'community': community})

        typeproduct = TypeProduct.objects.create(
            name=nome,
            community=community  # Associando o tipo de produto à comunidade
        )

        messages.success(request, f'Novo cultivo {typeproduct.name} criado com sucesso na comunidade {community.name}.')
        return redirect(f'/comunidades/dashboard/?community_id={community.id}')

    return render(request, 'create_typeproduct.html', {'community': community})

#---------------------------------------------DIVISAO-------------------------------------------------
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
