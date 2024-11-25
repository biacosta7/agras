from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from seedbeds.models import Seedbed
from communities.models import Community, MembershipRequest
from products.models import Product, TypeProduct
from areas.models import Area


@login_required
def create_seedbed(request, community_id, area_id):
    community = get_object_or_404(Community, id=community_id)
    area = get_object_or_404(Area, id=area_id, community=community)
    membership_requests = MembershipRequest.objects.filter(community=community, status='pending')

    if request.method == 'POST':
        seedbed_name = request.POST.get('seedbed_name')
        if seedbed_name:
            if Seedbed.objects.filter(nome=seedbed_name, area=area).exists():
                messages.error(request, 'Já existe um canteiro com esse nome nesta área. Por favor, escolha outro nome.')
            else:
                try:
                    Seedbed.objects.create(nome=seedbed_name, area=area)
                    messages.success(request, 'Canteiro criado com sucesso!')
                    return redirect('area_detail', community_id=community.id, area_id=area.id)
                except Exception as e:
                    messages.error(request, f'Erro ao criar o canteiro: {str(e)}')
        else:
            messages.error(request, 'Por favor, insira um nome válido para o canteiro.')

    context = {
        'community': community,
        'area': area,
        'membership_requests': membership_requests,
    }
    return render(request, 'create_seedbed.html', context)


@login_required
def edit_seedbed(request, community_id, area_id, seedbed_id):
    community = get_object_or_404(Community, id=community_id)
    area = get_object_or_404(Area, id=area_id, community=community)
    seedbed = get_object_or_404(Seedbed, id=seedbed_id, area=area)
    membership_requests = MembershipRequest.objects.filter(community=community, status='pending')

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

    context = {
        'community': community,
        'area': area,
        'seedbed': seedbed,
        'membership_requests': membership_requests,
    }
    return render(request, 'edit_seedbed.html', context)


@login_required
def delete_seedbed(request, community_id, area_id, seedbed_id):
    community = get_object_or_404(Community, id=community_id)
    area = get_object_or_404(Area, id=area_id, community=community)
    seedbed = get_object_or_404(Seedbed, id=seedbed_id, area=area)
    membership_requests = MembershipRequest.objects.filter(community=community, status='pending')

    if request.method == 'POST':
        seedbed.delete()
        messages.success(request, 'Canteiro deletado com sucesso!')
        return redirect('area_detail', community_id=community.id, area_id=area.id)

    context = {
        'seedbed': seedbed,
        'community': community,
        'area': area,
        'membership_requests': membership_requests,
    }
    return render(request, 'confirm_delete.html', context)


@login_required
def seedbed_detail_view(request, community_id, area_id, seedbed_id):
    community = get_object_or_404(Community, id=community_id)
    area = get_object_or_404(Area, id=area_id, community=community)
    seedbed = get_object_or_404(Seedbed, id=seedbed_id, area=area)
    membership_requests = MembershipRequest.objects.filter(community=community, status='pending')

    products = seedbed.products_in_seedbed.all()
    selected_product_id = request.GET.get('product_id')
    selected_product = products.filter(id=selected_product_id).first() if selected_product_id else products.first()

    context = {
        'community': community,
        'area': area,
        'seedbed': seedbed,
        'products': products,
        'selected_product': selected_product,
        'membership_requests': membership_requests,
    }

    return render(request, 'seedbed_detail.html', context)
