from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from seedbeds.models import Seedbed
from communities.models import Community  
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Product, TypeProduct
from areas.models import Area
from django.http import JsonResponse
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.utils.dateformat import DateFormat
from datetime import timedelta, datetime
from django.db.models import Sum, F

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
        seedbed_name = request.POST.get('seedbed_name')
        
        if seedbed_name:  # Verifica se o nome foi fornecido
            try:
                # Criação do canteiro
                Seedbed.objects.create(nome=seedbed_name, area=area)
                messages.success(request, 'Canteiro criado com sucesso!')
                return redirect('area_detail', community_id=community.id, area_id=area.id)  # Redireciona para a página de detalhes da área
            except Exception as e:
                # Caso ocorra algum erro ao criar o canteiro
                messages.error(request, f'Erro ao criar o canteiro: {str(e)}')
        else:
            messages.error(request, 'Por favor, insira um nome válido para o canteiro.')

    # Se o método não for POST, ou caso ocorra algum erro, redireciona para a página de detalhes da área
    return redirect('area_detail', community_id=community.id, area_id=area.id)

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
    community = get_object_or_404(Community, id=community_id)
    area = get_object_or_404(Area, id=area_id, community=community)
    seedbed = get_object_or_404(Seedbed, id=seedbed_id, area=area)

    # Obtém a lista de produtos associados ao canteiro
    active_products = seedbed.products_in_seedbed.filter(
        data_colheita__isnull=True,
    )
    print("All products in seedbed:", seedbed.products_in_seedbed.all().values('id', 'type_product__name', 'data_colheita', 'quantidade_colhida'))
    print("Active products:", active_products)
    # If you also want to track harvested products separately

    # Verifica se um produto foi selecionado a partir do dropdown
    # Handle product selection from dropdown (only from active products)
    selected_product_id = request.GET.get('product_id')
    if selected_product_id:
        selected_product = active_products.filter(id=selected_product_id).first()
    else:
        selected_product = active_products.first() if active_products else None
    
    # Verifica se o produto selecionado tem um ciclo de vida válido
    ciclo_de_vida = 3  # Valor padrão caso o ciclo de vida não esteja definido
    if selected_product and selected_product.type_product and selected_product.type_product.lifecycle is not None:
        ciclo_de_vida = selected_product.type_product.lifecycle

    estimativa_colheita = None
    if selected_product and selected_product.data_plantio and ciclo_de_vida:
        estimativa_colheita = selected_product.data_plantio + relativedelta(months=ciclo_de_vida)

    # Formatar a data antes de enviar para o template
    estimativa_colheita_formatada = (
        DateFormat(estimativa_colheita).format('d \d\e F \d\e Y') if estimativa_colheita else None
    )

    # Previsão de colheita
    previsao_colheita = None
    if selected_product and selected_product.type_product:
        tipo_produto = selected_product.type_product
        # Obtém o último produto colhido do mesmo tipo
        ultima_colheita = Product.objects.filter(
            type_product=tipo_produto, quantidade_colhida__isnull=False
        ).order_by('-data_colheita').first()

        if ultima_colheita and ultima_colheita.quantidade and ultima_colheita.quantidade_colhida:
            # Calcula a taxa com base na última colheita
            ultima_taxa = ultima_colheita.quantidade_colhida / ultima_colheita.quantidade
            # Previsão com base na quantidade plantada atual
            previsao_colheita = round(ultima_taxa * selected_product.quantidade)

    if request.method == 'POST' and 'quantidade_colhida' in request.POST:
        quantidade_colhida = int(request.POST.get('quantidade_colhida', 0))
        data_colheita_input = request.POST.get('harvest_date')

        if selected_product and selected_product.type_product:
            if selected_product.quantidade_colhida is None:
                selected_product.quantidade_colhida = 0
            
            # Atualizar quantidade colhida
            selected_product.quantidade_colhida += quantidade_colhida

            if data_colheita_input:
                data_colheita = datetime.strptime(data_colheita_input, "%Y-%m-%d").date()
                selected_product.data_colheita = data_colheita
            #selected_product.is_harvested = True
            selected_product.save()

            # Atualizar taxa de colheita do tipo de produto
            messages.success(request, f'{quantidade_colhida} unidades colhidas registradas para o tipo {tipo_produto.name}.')

    context = {
        'community': community,
        'area': area,
        'seedbed': seedbed,
        'products': active_products,  # This will show only non-harvested products
        'selected_product': selected_product,
        'estimativa_colheita': estimativa_colheita_formatada,
        'previsao_colheita': previsao_colheita,
        'active_products': active_products,
    }
    return render(request, 'seedbed_detail.html', context)

# def harvest_product_view(request, community_id, area_id, seedbed_id, product_id):
#     # Carrega as instâncias da comunidade, área, canteiro e produto
#     community = get_object_or_404(Community, id=community_id)
#     area = get_object_or_404(Area, id=area_id, community=community)
#     seedbed = get_object_or_404(Seedbed, id=seedbed_id, area=area)
#     product = get_object_or_404(Product, id=product_id, seedbed=seedbed)

#     if request.method == 'POST':
#         quantidade_colhida = int(request.POST.get('quantidade_colhida', 0))
#         if product and product.type_product:
#             # Cria uma nova colheita
#             Product.objects.create(
#                 type_product=product.type_product,
#                 seedbed=seedbed,
#                 quantidade_colhida=quantidade_colhida,
#                 data_colheita=timezone.now()
#             )
#             messages.success(request, f'{quantidade_colhida} unidades colhidas registradas para o tipo {product.type_product.name}.')

#     # Redireciona de volta para a página de detalhes do canteiro após salvar a colheita
#     return redirect('seedbed_detail', community_id=community.id, area_id=area.id, seedbed_id=seedbed.id)