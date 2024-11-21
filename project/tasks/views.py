from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.utils import timezone
from .models import Task
from users.models import User
from products.models import Product, TypeProduct
from areas.models import Area
from seedbeds.models import Seedbed
from communities.models import Community
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse

def add_task(request, community_id, area_id=None, seedbed_id=None, product_id=None, type_product_id=None):
    community = get_object_or_404(Community, id=community_id)
    users = community.members.all().union(community.admins.all()) if community else None

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_completed = request.POST.get('is_completed') == 'on'
        start_date = request.POST.get('start_date')
        deadline = request.POST.get('deadline')
        recurrence = request.POST.get('recurrence')
        priority = request.POST.get('priority')
        responsible_user_ids = request.POST.getlist('responsible_users[]')
        print(request.POST)  # Adiciona esta linha para inspecionar os dados recebidos

        if not title or not deadline or not start_date:
            print('Título e data são obrigatórios.')
            return JsonResponse({'error': 'Título e data de vencimento são obrigatórios.'}, status=400)
        
        try:
            start_date = timezone.datetime.strptime(start_date, '%d-%m-%Y')
            deadline = timezone.datetime.strptime(deadline, '%d-%m-%Y')
        except ValueError:
            print("Formato de data inválido. Use 'DD/MM/AAAA")
            return JsonResponse({'error': "Formato de data inválido. Use 'DD/MM/AAAA'."}, status=400)

        # Cria a tarefa
        task = Task(
            title=title,
            description=description,
            is_completed=is_completed,
            start_date = start_date,
            deadline=deadline,
            recurrence=recurrence,
            status='to_do', 
            priority=priority,
            community=community,
            # area_id=area_id,
            # seedbed_id=seedbed_id,
            # product_id=product_id,
            # type_product_id=type_product_id,
        )
        task.save()

        # Configura o relacionamento many-to-many para usuários responsáveis
        if responsible_user_ids:
            user_ids = [int(uid) for uid in responsible_user_ids if uid]
            users = User.objects.filter(id__in=user_ids)
            task.responsible_users.set(users)

        # Resposta AJAX de sucesso
        messages.success(request, "Tarefa adicionada com sucesso!")
        return JsonResponse({'success': 'Tarefa adicionada com sucesso!'})

    # Geração da URL para o formulário
    kwargs = {key: val for key, val in [
        ('community_id', community_id),
        ('area_id', area_id),
        ('seedbed_id', seedbed_id),
        ('product_id', product_id),
        ('type_product_id', type_product_id)
    ] if val is not None}

    form_url = reverse('add_task', kwargs=kwargs)

    # Renderiza o modal de formulário via AJAX
    context = {
        'form_url': form_url,
        'product_id': product_id,
        'community_id': community_id,
        'area_id': area_id,
        'seedbed_id': seedbed_id,
        'type_product_id': type_product_id,
        'users': users
    }

    if request.is_ajax():
        return render(request, 'add_task.html', context)

    return render(request, 'dashboard.html', context)

# def view_tasks(request, community_id=None, area_id=None, seedbed_id=None, product_id=None, type_product_id=None):
#     tasks = Task.objects.all()

#     context = {
#         'tasks': tasks,
#         'product_id': product_id,
#         'community_id': community_id,
#         'area_id': area_id,
#         'seedbed_id': seedbed_id,
#         'type_product_id': type_product_id,
#     }

#     return render(request, 'view_tasks.html', context)

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