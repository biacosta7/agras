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


def add_task(request, community_id, area_id=None, seedbed_id=None, product_id=None, type_product_id=None):
    task_type = request.POST.get('type')
    
    community = get_object_or_404(Community, id=community_id)
    # area = get_object_or_404(Area, id=area_id, community=community) if area_id else None
    # seedbed = get_object_or_404(Seedbed, id=seedbed_id, area=area) if seedbed_id else None
    # product = get_object_or_404(Product, id=product_id, seedbed=seedbed) if product_id else None
    # type_product = get_object_or_404(TypeProduct, id=type_product_id) if type_product_id else None
    users = community.members.all().union(community.admins.all()) if community else None

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_completed = request.POST.get('is_completed') == 'on'
        deadline = request.POST.get('deadline')
        recurrence = request.POST.get('recurrence')
        status = request.POST.get('status')
        priority = request.POST.get('priority')
        responsible_user_ids = request.POST.getlist('responsible_users[]')


        #fazer recorrencia nao ser obrigatoria
        if not title or not deadline or not recurrence:
            return HttpResponseBadRequest("Todos os campos são obrigatórios.")

        try:
            deadline = timezone.datetime.strptime(deadline, '%d/%m/%Y')  # Formato de data sem hora
        except ValueError:
            return HttpResponseBadRequest("Formato inválido. Use 'DD/MM/AAAA'.")
        task = Task(
            #type=task_type,
            title=title,
            description=description,
            is_completed=is_completed,
            deadline=deadline,
            recurrence=recurrence,
            status=status,
            priority=priority,
        )

        # if task_type == 'community' and community:
        #     task.community = community
        # elif task_type == 'area' and area:
        #     task.area = area
        # elif task_type == 'seedbed' and seedbed:
        #     task.seedbed = seedbed
        # elif task_type == 'product' and product:
        #     task.product = product
        # elif task_type == 'type_product' and type_product:
        #     task.type_product = type_product
        # else:
        #     return HttpResponseBadRequest("Tipo inválido ou não encontrado.")

        task.save()

        # Then set the many-to-many relationship
        if responsible_user_ids:
            # Convert IDs to integers and filter out empty strings
            user_ids = [int(uid) for uid in responsible_user_ids if uid]
            # Get the user objects
            users = User.objects.filter(id__in=user_ids)
            # Set the many-to-many relationship
            task.responsible_users.set(users)

        messages.success(request, "Tarefa adicionada com sucesso!")
        # Gerar a URL para redirecionar para o dashboard, com os parâmetros necessários
        redirect_url = reverse('dashboard', kwargs={'community_id': community_id})
        return redirect(redirect_url)

    # Criar um dicionário de kwargs, omitindo parâmetros que são None
    kwargs = {}
    if community_id:
        kwargs['community_id'] = community_id
    if area_id:
        kwargs['area_id'] = area_id
    if seedbed_id:
        kwargs['seedbed_id'] = seedbed_id
    if product_id:
        kwargs['product_id'] = product_id
    if type_product_id:
        kwargs['type_product_id'] = type_product_id

    # Gerar a URL para o formulário
    form_url = reverse('add_task', kwargs=kwargs)

    context = {
        'form_url': form_url,
        'product_id': product_id,
        'community_id': community_id,
        'area_id': area_id,
        'seedbed_id': seedbed_id,
        'type_product_id': type_product_id,
        'users': users
    }

    return render(request, 'add_task.html', context)

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