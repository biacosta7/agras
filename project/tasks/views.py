from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.utils import timezone
from .models import Task
from products.models import Product
from areas.models import Area
from seedbeds.models import Seedbed
from communities.models import Community

def add_task(request, community_id, area_id, seedbed_id, product_id):
    community = get_object_or_404(Community, id=community_id)
    area = get_object_or_404(Area, id=area_id, community=community)
    seedbed = get_object_or_404(Seedbed, id=seedbed_id, area=area)
    product = get_object_or_404(Product, id=product_id, seedbed=seedbed)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_completed = request.POST.get('is_completed') == 'on'  
        deadline = request.POST.get('deadline')
        recurrence = request.POST.get('recurrence')
        time = request.POST.get('time')

        # Validação dos campos obrigatórios
        if not title or not deadline or not recurrence or not time:
            return HttpResponseBadRequest("Todos os campos são obrigatórios.")

        try:
            deadline = timezone.datetime.strptime(deadline, '%d/%m/%Y %H:%M')
        except ValueError:
            return HttpResponseBadRequest("Formato inválido. Use 'DD/MM/AAAA HH:MM'.")

        # Criação da Task
        task = Task(
            product=product,
            title=title,
            description=description,
            is_completed=is_completed,
            deadline=deadline,
            recurrence=recurrence,
            time=time,
        )
        task.save()

        # Redireciona para a página de detalhes do produto com os IDs como parâmetros
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
    }
    return render(request, 'add_task.html', context)
