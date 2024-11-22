from django.shortcuts import redirect, render, get_object_or_404
from django.db import IntegrityError
from .models import Task
from products.models import Product, TypeProduct
from areas.models import Area
from seedbeds.models import Seedbed
from communities.models import Community
from django.contrib import messages
from users.models import User

def task_page(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    all_areas_in_specific_community = Area.objects.filter(community=community)
    all_seedbeds_in_specific_area = Seedbed.objects.filter(area__in=all_areas_in_specific_community)
    
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        local = request.POST.get('local')
        start_date = request.POST.get('start_date')
        final_date = request.POST.get('final_date')
        priority = request.POST.get('priority')
        status = request.POST.get('status')
        responsible_users_raw = request.POST.get('responsible_users[]', '')
        responsible_users_ids = responsible_users_raw.split(',') if responsible_users_raw else []
        
        if start_date > final_date:
            messages.error(request, "A data final não pode ser antes da data inicial.")
            return redirect('task_page', community_id=community_id)

        try:
            responsible_users_ids = [int(id.strip()) for id in responsible_users_ids]
        except ValueError:
            messages.error(request, "IDs inválidos fornecidos para usuários responsáveis.")
            responsible_users_ids = []

        if not description or not local or not start_date or not priority or not status or not responsible_users_ids:
            messages.error(request, 'Todos os campos são obrigatórios.')
        else:
            try:
                task = Task.objects.create(
                    title=title,
                    community=community, 
                    description=description,
                    local=local,
                    start_date=start_date,
                    final_date= final_date,
                    priority=priority,
                    status=status,
                )

                responsible_users = User.objects.filter(id__in=responsible_users_ids)
                task.responsible_users.set(responsible_users)

                messages.success(request, 'Tarefa criada com sucesso.')
                return redirect('task_page', community_id=community_id)
            except Exception as e:
                messages.error(request, f'Erro ao criar tarefa: {e}')


    tasks = Task.objects.filter(community=community) # Buscando as tarefas depois do processamento do POST

    context = {
        'tasks': tasks,
        'community': community,
        'all_areas': all_areas_in_specific_community,
        'all_seedbeds': all_seedbeds_in_specific_area,
        'status_choices': Task.STATUS_CHOICES,
        'priority_choices': Task.PRIORITY,
        'place_choices': Task.TYPE_CHOICES
    }
    return render(request, 'tasks.html', context)

def list_tasks(request, community_id, area_id=None, seedbed_id=None, product_id=None):
    # Filtros iniciais
    tasks = Task.objects.all()

    community = get_object_or_404(Community, id=community_id)
    tasks = tasks.filter(community=community)

    # Filtrando com base no area_id, seedbed_id, e product_id (se fornecido)
    if area_id:
        area = get_object_or_404(Area, id=area_id)
        tasks = tasks.filter(area=area)

    if seedbed_id:
        seedbed = get_object_or_404(Seedbed, id=seedbed_id)
        tasks = tasks.filter(seedbed=seedbed)

    if product_id:
        product = get_object_or_404(Product, id=product_id)
        tasks = tasks.filter(product=product)

    # Passando os dados para o template
    return render(request, 'list_task.html', {
        'tasks': tasks,
        'community': community,
        'area': area if area_id else None,
        'seedbed': seedbed if seedbed_id else None,
        'product': product if product_id else None,
    })