from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Product, TypeProduct
from django.contrib import messages
from django.core.exceptions import ValidationError
from communities.models import Community
from seedbeds.models import Seedbed
from areas.models import Area
from django.http import JsonResponse

@login_required  
def create_product_view(request, seedbed_id, community_id, area_id):
    # Buscar a comunidade
    community = get_object_or_404(Community, id=community_id)

    # Buscar a área e garantir que pertence à comunidade
    try:
        area = Area.objects.get(id=area_id, community=community)
    except Area.DoesNotExist:
        messages.error(request, f'A área com ID {area_id} não pertence à comunidade com ID {community_id}.')
        return redirect('dashboard', community_id)

    # Buscar o canteiro e garantir que pertence à área correta
    seedbed = get_object_or_404(Seedbed, id=seedbed_id, area=area)

    # Filtrar tipos de produtos por comunidade
    tipos_produtos = TypeProduct.objects.filter(community=community)

    if request.method == 'POST':
        type_name = request.POST.get('type_name')
        quantity = request.POST.get('quantity')
        planting_date = request.POST.get('planting_date')

        # Verificar se o tipo de produto existe na comunidade
        type_product = get_object_or_404(TypeProduct, name=type_name, community=community)

        errors = []

        # Validação dos campos
        if not type_name:
            errors.append("O campo 'Cultivo' é obrigatório.")
        if not planting_date:
            errors.append("O campo 'Data de plantio' é obrigatório.")
        if not quantity:
            errors.append("O campo 'Quantidade' é obrigatório.")
        elif not quantity.isdigit():
            errors.append("O campo 'Quantidade' deve ser um número válido.")
        
        if errors:
            return render(request, 'create_product.html', {
                'errors': errors,
                'community': community,
                'tipos_produtos': tipos_produtos,  
                'seedbed': seedbed,
            })

        try:
            # Criar o produto associado à comunidade
            product = Product.objects.create(
                type_product=type_product,
                seedbed=seedbed, 
                quantidade=int(quantity),
                data_plantio=planting_date
            )
            messages.success(request, f'Produto {product.type_product.name} cadastrado com sucesso no canteiro {seedbed.nome}.')

        except ValidationError as e:
            messages.error(request, f"Erro de validação: {e}")

        return redirect('seedbed_detail', community_id=community.id, area_id=area_id, seedbed_id=seedbed_id)
    
    context = {
        'community': community, 
        'tipos_produtos': tipos_produtos,
        'seedbed': seedbed,
        'area': area,
    }

    return render(request, 'create_product.html', context)


@login_required  
def create_typeproduct_view(request, community_id, area_id, seedbed_id):
    community = get_object_or_404(Community, id=community_id)

    if request.method == 'POST':
        nome = request.POST.get('nome').capitalize()
        
        # Verificando se o tipo de produto já existe na mesma comunidade
        if TypeProduct.objects.filter(name=nome, community=community).exists():
            messages.error(request, f'O cultivo {nome} já existe na comunidade {community.name}. Por favor, escolha um nome diferente.')
            return render(request, 'create_typeproduct.html', {'community': community, 'area_id': area_id, 'seedbed_id': seedbed_id})

        typeproduct = TypeProduct.objects.create(
            name=nome,
            community=community  # Associando o tipo de produto à comunidade
        )

        messages.success(request, f'Novo cultivo {typeproduct.name} criado com sucesso na comunidade {community.name}.')
        return redirect('seedbed_detail', community_id=community.id, area_id=area_id, seedbed_id=seedbed_id)
    return render(request, 'create_typeproduct.html', {'community': community, 'area_id': area_id, 'seedbed_id': seedbed_id})

#---------------------------------------------DIVISAO-------------------------------------------------
def product_list_view(request, seedbed_id, community_id, area_id):
    # Obtém o canteiro com base no ID passado na URL
    seedbed = get_object_or_404(Seedbed, id=seedbed_id)
    community = get_object_or_404(Community, id=community_id)
    area = get_object_or_404(Area, id=area_id)  # Obtendo a área se necessário

    # Filtra os produtos que pertencem ao canteiro
    queryset = Product.objects.filter(seedbed=seedbed)

    context = {
        'object_list': queryset,
        'seedbed': seedbed,  
        'community': community,
        'area': area  # Se você precisar passar a área para o template
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

    # Verificar se o canteiro pertence à comunidade
    if product.seedbed.community != seedbed.community:
        messages.error(request, "Você não tem permissão para editar este produto.")
        return redirect('product:product-list', seedbed.id)

    type_products = TypeProduct.objects.all()

    if request.method == "GET":
        return render(request, 'edit_product.html', {
            'product': product,
            'type_products': type_products,
            'seedbed': seedbed
        })

    else:
        nome = request.POST.get('nome')
        data_plantio = request.POST.get('data_plantio')
        quantidade = request.POST.get('quantidade')

        # Atualizando o produto com a nova informação
        type_product = get_object_or_404(TypeProduct, name=nome)
        product.type_product = type_product  # Corrigido para usar `type_product`
        product.planting_date = data_plantio
        product.quantity = quantidade    
        product.save()

        messages.success(request, 'Cultivo editado com sucesso.')

        return redirect('product:product-list', seedbed.id)


@login_required
def product_delete_view(request, community_id, area_id, seedbed_id, product_id):
    # Obtendo o seedbed e o product
    seedbed = get_object_or_404(Seedbed, id=seedbed_id)
    product = get_object_or_404(Product, id=product_id)
    community = get_object_or_404(Community, id=community_id)

    # Verificar se o canteiro pertence à comunidade através da área
    if seedbed.area.community != community:  # Verificação correta
        messages.error(request, "Você não tem permissão para deletar este produto.")
        return redirect('product:product_list', community_id=community.id, seedbed_id=seedbed.id)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Produto deletado com sucesso.')
        return redirect('seedbed_detail', community_id=community.id, area_id=area_id, seedbed_id=seedbed.id)

    context = {
        'product': product,
        'seedbed': seedbed,
        'community': community,
    }

    return render(request, 'delete_product.html', context)



def product_update_view(request, seedbed_id, product_id, community_id):
    seedbed = get_object_or_404(Seedbed, id=seedbed_id)
    product = get_object_or_404(Product, id=product_id)
    community = get_object_or_404(Community, id=community_id)

    type_products = TypeProduct.objects.filter(community=community)

    if request.method == "GET":
        return render(request, 'edit_product.html', {'product': product, 'type_products': type_products, 'seedbed': seedbed, 'community': community})

    else:
        nome = request.POST.get('nome')
        data_plantio = request.POST.get('data_plantio')
        quantidade = request.POST.get('quantidade')

        # Atualizando o produto com a nova informação
        try:
            type_product = TypeProduct.objects.get(name=nome, community=community)   
            product.type_product = type_product
        except TypeProduct.DoesNotExistw:
            messages.error(request, 'Tipo de produto não encontrado')
            return redirect('product:product_update_view', seedbed_id, product_id, community_id)
        product.data_plantio = data_plantio
        product.quantidade = quantidade    
        product.save()

        messages.success(request, 'Cultivo editado com sucesso.')

        return redirect('product:product_list', community_id, seedbed.id)
    
def get_product_info_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Formatar os dados em um dicionário para retornar como JSON
    data = {
        'data_plantio': product.data_plantio.strftime('%d/%m/%Y'),  # Formato de data legível
        'estimativa_colheita': '10/12/2024',  # Você pode ajustar isso com base no produto
        'quantidade': product.quantidade,
    }
    
    return JsonResponse(data)