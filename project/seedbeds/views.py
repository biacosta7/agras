from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from seedbeds.models import Seedbed
from communities.models import Community  
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Product, TypeProduct
from areas.models import Area
from django.http import JsonResponse


@login_required
def list_seedbeds(request, community_id, area_id):
    community = get_object_or_404(Community, id=community_id)
    area = get_object_or_404(Area, id=area_id, community=community)  # Filtra pela área da comunidade
    canteiros = Seedbed.objects.filter(area=area)  # Filtra os canteiros pela área
    return render(request, 'list_seedbeds.html', {'canteiros': canteiros, 'community': community, 'area': area})

@login_required
def create_seedbed(request, community_id, area_id):
    user = request.user
    communities = user.communities_members.all()  # Obtém todas as comunidades do usuário

    # Obter a comunidade específica selecionada
    community = get_object_or_404(Community, id=community_id)

    # Tenta obter a área específica, evitando MultipleObjectsReturned
    area = get_object_or_404(Area, id=area_id, community=community)

    if request.method == 'POST':
        # Obter o nome do canteiro
        seedbed_name = request.POST.get('seedbed_name')  # Certifique-se de que este campo está no formulário
        if seedbed_name:
            # Criação do canteiro
            Seedbed.objects.create(nome=seedbed_name, area=area)

            messages.success(request, 'Canteiro criado com sucesso!')
            return redirect('area_detail', community_id=community.id, area_id=area.id)  # Redirecionar para a lista de canteiros da comunidade
        else:
            messages.error(request, 'Por favor, insira um nome válido para o canteiro.')

    context = {
        'communities': communities,
        'community': community,
        'area': area,  # Adiciona a área ao contexto
    }
    return render(request, 'create_seedbed.html', context)

@login_required
def edit_seedbed(request, community_id, area_id, seedbed_id):
    community = get_object_or_404(Community, id=community_id)
    area = get_object_or_404(Area, id=area_id, community=community)
    seedbed = get_object_or_404(Seedbed, id=seedbed_id, area=area)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        if nome:
            if Seedbed.objects.filter(nome=nome, area=area).exclude(id=seedbed_id).exists():
                messages.error(request, 'Já existe um canteiro com esse nome nesta área. Por favor, tente novamente.')
            else:
                seedbed.nome = nome
                seedbed.save()
                messages.success(request, 'Canteiro editado com sucesso!')
                return redirect('area_detail', community_id=community.id, area_id=area.id)

    return render(request, 'edit_seedbed.html', {'seedbed': seedbed, 'community': community, 'area': area})

@login_required
def delete_seedbed(request, community_id, area_id, seedbed_id):
    # Buscando o canteiro e a comunidade correspondente
    community = get_object_or_404(Community, id=community_id)
    area = get_object_or_404(Area, id=area_id, community=community)
    seedbed = get_object_or_404(Seedbed, id=seedbed_id, area=area)

    if request.method == 'POST':
        seedbed.delete()  # Deletando o canteiro
        messages.success(request, 'Canteiro deletado com sucesso!')
        # Redirecionando para a lista de canteiros, passando o ID da comunidade
        return redirect('area_detail', community_id=community_id, area_id=area_id)
    
    # Caso não seja POST, renderizar uma página de confirmação
    context = {
        'seedbed': seedbed,
        'community': community,
        'area': area
    }
    return render(request, 'confirm_delete.html', context)


def seedbed_detail_view(request, community_id, area_id, seedbed_id):
    # Obtém a comunidade, área e o canteiro
    community = get_object_or_404(Community, id=community_id)
    area = get_object_or_404(Area, id=area_id, community=community)
    seedbed = get_object_or_404(Seedbed, id=seedbed_id, area=area)

    # Obtém a lista de produtos associados ao canteiro
    products = seedbed.products_in_seedbed.all()

    # Verifica se um produto foi selecionado a partir do dropdown
    selected_product_id = request.GET.get('product_id')
    if selected_product_id:
        try:
            selected_product = products.get(id=selected_product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Produto não encontrado'}, status=404)
        
        # Retorna os dados do produto selecionado como JSON
        data = {
            'planting_date': selected_product.data_plantio,
            'quantity': selected_product.quantidade,
            'harvest_estimate': '10/12/2024',  # Substitua conforme sua lógica
            'comments': 'Excelente desenvolvimento até agora!',  # Ajuste conforme necessário
        }
        return JsonResponse(data)

    # Se não houver produto selecionado, define o primeiro produto como padrão
    selected_product = products.first() if products else None

    context = {
        'community': community,
        'area': area,
        'seedbed': seedbed,
        'products': products,
        'selected_product': selected_product,  # Assegure-se de que selected_product está incluído
    }
    
    return render(request, 'seedbed_detail.html', context)
