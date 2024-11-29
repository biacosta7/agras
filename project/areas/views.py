from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from .models import Area
from tasks.models import Task
from communities.models import Community, MembershipRequest
from seedbeds.models import Seedbed
from products.models import Product, TypeProduct
from django.contrib import messages
from collections import defaultdict
from django.shortcuts import render

# View para listar as áreas
def area_manage(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    # áreas que pertencem à comunidade
    areas = community.areas.all()

    # Cria uma lista com áreas e suas respectivas tarefas pendentes
    areas_with_pending_tasks = []
    for area in areas:
        pending_tasks_count = Task.objects.filter(status="Pendente", area=area, local='area').count()
        areas_with_pending_tasks.append({
            'area': area,
            'pending_tasks': pending_tasks_count
        })

    # Recupera as solicitações pendentes para a comunidade
    membership_requests = MembershipRequest.objects.filter(community=community, status='pending')

    # Verifica se o usuário logado é admin
    is_admin_of_community = request.user.admin_communities.exists()

    return render(request, 'area_manage.html', {
        'areas': areas,
        'community': community,
        'membership_requests': membership_requests,
        'is_admin_of_community': is_admin_of_community,
        'areas_with_pending_tasks': areas_with_pending_tasks
    })


# View para criar uma nova área
def area_create(request, communities_id):
    # Recupera a comunidade correspondente ao ID fornecido
    community = get_object_or_404(Community, id=communities_id)

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Verifica se já existe uma área com o mesmo nome na comunidade
        if Area.objects.filter(name=name, community=community).exists():
            messages.error(request, 'Uma área com esse nome já existe nesta comunidade. Por favor, escolha outro nome.')
            return redirect('area_manage', community_id=communities_id)

        try:
            # Cria a nova área associada à comunidade
            area = Area.objects.create(
                name=name,
                description=description,
                community=community
            )
            messages.success(request, 'Área criada com sucesso.')
            return redirect('area_manage', community_id=communities_id)  # Redireciona para a lista de áreas da comunidade
        
        except IntegrityError:
            messages.error(request, 'Erro ao criar a área. Tente novamente.')
            return redirect('area_manage', community_id=communities_id)

    return redirect('area_manage', community_id=communities_id)


# View para editar uma área existente
def area_edit(request, community_id, pk):
    # Recupera a área correspondente ao ID fornecido
    area = get_object_or_404(Area, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Se o nome e a descrição estiverem presentes, atualize a área
        if name and description:
            area.name = name
            area.description = description
            area.save()
            messages.success(request, 'Área atualizada com sucesso.')
            return redirect('area_manage', community_id=area.community.id)  # Redireciona para a lista de áreas da comunidade correspondente

    # Recupera as comunidades para mostrar no template
    communities = Community.objects.all()
    
    return render(request, 'area_manage.html', {
        'area': area,
        'communities': communities,
        'community': area.community,  # Adiciona a comunidade correspondente ao contexto
    })

# View para deletar uma área
def area_delete(request, community_id, pk):
    area = get_object_or_404(Area, pk=pk)

    if request.method == 'POST':
        area.delete()
        messages.success(request, 'Área deletada com sucesso.')
        return redirect('area_manage', community_id=area.community.id)  # Redireciona para a lista de áreas da comunidade correspondente

    return render(request, 'area_manage.html', {'area': area})


def area_detail(request, community_id, area_id):
    community = get_object_or_404(Community, id=community_id)
    area = get_object_or_404(Area, id=area_id, community=community)
    is_admin_of_community = request.user.admin_communities.exists()
    # Recuperando os canteiros (seedbeds) associados à área
    seedbeds = Seedbed.objects.filter(area=area)

    membership_requests = MembershipRequest.objects.filter(community=community, status='pending')


    # Cria uma lista com áreas e suas respectivas tarefas pendentes
    seedbeds_with_pending_tasks = []
    for seedbed in seedbeds:
        pending_tasks_count = Task.objects.filter(status="Pendente", seedbed=seedbed, local="seedbed").count()
        seedbeds_with_pending_tasks.append({
            'seedbed': seedbed,
            'pending_tasks': pending_tasks_count
        })

    context = {
        'community': community,
        'area': area,
        'seedbeds': seedbeds,
        'membership_requests': membership_requests,
        'is_admin_of_community': is_admin_of_community,
        'seedbeds_with_pending_tasks': seedbeds_with_pending_tasks
    }
    return render(request, 'area_detail.html', context)