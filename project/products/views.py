from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Product, TypeProduct
from django.contrib import messages
from django.core.exceptions import ValidationError
from communities.models import Community, MembershipRequest
from seedbeds.models import Seedbed
from areas.models import Area

@login_required  
def create_product_view(request, seedbed_id, community_id, area_id):
    community = get_object_or_404(Community, id=community_id)

    try:
        area = Area.objects.get(id=area_id, community=community)
    except Area.DoesNotExist:
        messages.error(request, f'A área com ID {area_id} não pertence à comunidade com ID {community_id}.')
        return redirect('dashboard', community_id)

    seedbed = get_object_or_404(Seedbed, id=seedbed_id, area=area)
    tipos_produtos = TypeProduct.objects.filter(community=community)
    membership_requests = MembershipRequest.objects.filter(community=community, status='pending')

    if request.method == 'POST':
        type_name = request.POST.get('type_name')
        quantity = request.POST.get('quantity')
        planting_date = request.POST.get('planting_date')

        type_product = get_object_or_404(TypeProduct, name=type_name, community=community)

        errors = []
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
                'membership_requests': membership_requests,
            })

        try:
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
        'membership_requests': membership_requests,
    }
    return render(request, 'create_product.html', context)


@login_required  
def create_typeproduct_view(request, community_id, area_id, seedbed_id):
    community = get_object_or_404(Community, id=community_id)
    membership_requests = MembershipRequest.objects.filter(community=community, status='pending')

    if request.method == 'POST':
        nome = request.POST.get('nome').capitalize()
        
        if TypeProduct.objects.filter(name=nome, community=community).exists():
            messages.error(request, f'O cultivo {nome} já existe na comunidade {community.name}. Por favor, escolha um nome diferente.')
            return render(request, 'create_typeproduct.html', {
                'community': community,
                'membership_requests': membership_requests,
                'area_id': area_id,
                'seedbed_id': seedbed_id
            })

        typeproduct = TypeProduct.objects.create(
            name=nome,
            community=community
        )
        messages.success(request, f'Novo cultivo {typeproduct.name} criado com sucesso na comunidade {community.name}.')
        return redirect('seedbed_detail', community_id=community.id, area_id=area_id, seedbed_id=seedbed_id)

    return render(request, 'create_typeproduct.html', {
        'community': community,
        'membership_requests': membership_requests,
        'area_id': area_id,
        'seedbed_id': seedbed_id
    })


@login_required
def product_list_view(request, seedbed_id, community_id, area_id):
    seedbed = get_object_or_404(Seedbed, id=seedbed_id)
    community = get_object_or_404(Community, id=community_id)
    area = get_object_or_404(Area, id=area_id)
    membership_requests = MembershipRequest.objects.filter(community=community, status='pending')
    queryset = Product.objects.filter(seedbed=seedbed)

    context = {
        'object_list': queryset,
        'seedbed': seedbed,  
        'community': community,
        'membership_requests': membership_requests,
        'area': area
    }
    return render(request, "product_list.html", context)


@login_required
def product_update_view(request, community_id, area_id, seedbed_id, product_id):
    seedbed = get_object_or_404(Seedbed, id=seedbed_id)
    product = get_object_or_404(Product, id=product_id)
    community = get_object_or_404(Community, id=community_id)
    area = get_object_or_404(Area, id=area_id)

    if seedbed.area != area or area.community != community:
        messages.error(request, "Você não tem permissão para editar este produto.")
        return redirect('seedbed_detail', community_id=community.id, area_id=area.id, seedbed_id=seedbed_id)

    membership_requests = MembershipRequest.objects.filter(community=community, status='pending')
    type_products = TypeProduct.objects.filter(community=community)

    if request.method == "GET":
        return render(request, 'seedbed_detail.html', {
            'community': community,
            'product': product,
            'type_products': type_products,
            'seedbed': seedbed,
            'area': area,
            'membership_requests': membership_requests,
        })

    else:
        data_plantio = request.POST.get('data_plantio')
        quantidade = request.POST.get('quantidade')

        errors = []
        if not data_plantio:
            errors.append("O campo 'Data de plantio' é obrigatório.")
        if not quantidade:
            errors.append("O campo 'Quantidade' é obrigatório.")
        elif not quantidade.isdigit():
            errors.append("O campo 'Quantidade' deve ser um número válido.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('product_update', community_id=community_id, area_id=area_id, seedbed_id=seedbed_id, product_id=product_id)

        product.data_plantio = data_plantio
        product.quantidade = int(quantidade)
        product.save()
        messages.success(request, 'Cultivo editado com sucesso.')

        return redirect('seedbed_detail', community_id=community.id, area_id=area.id, seedbed_id=seedbed.id)


@login_required
def product_delete_view(request, community_id, area_id, seedbed_id, product_id):
    seedbed = get_object_or_404(Seedbed, id=seedbed_id)
    product = get_object_or_404(Product, id=product_id)
    community = get_object_or_404(Community, id=community_id)

    if seedbed.area.community != community:
        messages.error(request, "Você não tem permissão para deletar este produto.")
        return redirect('product:product_list', community_id=community.id, seedbed_id=seedbed.id)

    membership_requests = MembershipRequest.objects.filter(community=community, status='pending')

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Produto deletado com sucesso.')
        return redirect('seedbed_detail', community_id=community.id, area_id=area_id, seedbed_id=seedbed.id)

    context = {
        'product': product,
        'seedbed': seedbed,
        'community': community,
        'membership_requests': membership_requests,
    }
    return render(request, 'delete_product.html', context)

def get_product_info_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Formatar os dados em um dicionário para retornar como JSON
    data = {
        'data_plantio': product.data_plantio.strftime('%d/%m/%Y'),  # Formato de data legível
        'estimativa_colheita': '10/12/2024',  # Você pode ajustar isso com base no produto
        'quantidade': product.quantidade,
    }
    
    return JsonResponse(data)