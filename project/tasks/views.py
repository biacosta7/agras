from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.utils import timezone
from .models import Task
from products.models import Product, TypeProduct
from areas.models import Area
from seedbeds.models import Seedbed
from communities.models import Community

def add_task(request, community_id=None, area_id=None, seedbed_id=None, product_id=None, type_product_id=None):
    task_type = request.POST.get('type')
    
    # busca a instancia correspondente ao tipo de task
    community = get_object_or_404(Community, id=community_id) if community_id else None
    area = get_object_or_404(Area, id=area_id, community=community) if area_id else None
    seedbed = get_object_or_404(Seedbed, id=seedbed_id, area=area) if seedbed_id else None
    product = get_object_or_404(Product, id=product_id, seedbed=seedbed) if product_id else None
    type_product = get_object_or_404(TypeProduct, id=type_product_id) if type_product_id else None

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_completed = request.POST.get('is_completed') == 'on'
        deadline = request.POST.get('deadline')
        recurrence = request.POST.get('recurrence')
        status = request.POST.get('status')

        # validacao dos campos obrigatorios
        if not title or not deadline or not recurrence:
            return HttpResponseBadRequest("Todos os campos são obrigatórios.")

        try:
            deadline = timezone.datetime.strptime(deadline, '%d/%m/%Y %H:%M')
        except ValueError:
            return HttpResponseBadRequest("Formato inválido. Use 'DD/MM/AAAA HH:MM'.")

        task = Task(
            type=task_type,
            title=title,
            description=description,
            is_completed=is_completed,
            deadline=deadline,
            recurrence=recurrence,
            status=status,
        )
        
        # atribui o campo correspondente ao tipo
        if task_type == 'community' and community:
            task.community = community
        elif task_type == 'area' and area:
            task.area = area
        elif task_type == 'seedbed' and seedbed:
            task.seedbed = seedbed
        elif task_type == 'product' and product:
            task.product = product
        elif task_type == 'type_product' and type_product:
            task.type_product = type_product
        else:
            return HttpResponseBadRequest("Tipo inválido ou não encontrado.")

        task.save()

        return redirect(
            'product_detail', 
            community_id=community_id, 
            area_id=area_id, 
            seedbed_id=seedbed_id, 
            product_id=product_id
        )

    context = {
        'product_id': product_id,
        'community_id': community_id,
        'area_id': area_id,
        'seedbed_id': seedbed_id,
        'type_product_id': type_product_id,
    }
    return render(request, 'add_task.html', context)
