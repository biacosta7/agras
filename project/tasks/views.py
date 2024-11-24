from datetime import timedelta
from django.utils import timezone
from django.utils.timezone import now
from django.shortcuts import redirect, render, get_object_or_404
from .models import Task
from products.models import Product, TypeProduct
from areas.models import Area
from seedbeds.models import Seedbed
from communities.models import Community, MembershipRequest
from django.contrib import messages
from users.models import User

def calculate_final_date(start_date, recurrence):   
    today = now().date()  # Obtém a data atual
    if recurrence == 'Única':
        final_date = start_date
    elif recurrence == 'Diária':
        final_date = start_date + timedelta(days=1)
    elif recurrence == 'Semanal':
        weeks_diff = (today - start_date).days // 7
        final_date = start_date + timedelta(weeks=(weeks_diff + 1))
    elif recurrence == 'Mensal':
        if start_date.month < 12:
            final_date = start_date.replace(month=start_date.month + 1)
        else:
            final_date = start_date.replace(month=1, year=start_date.year + 1)
    elif recurrence == 'Anual':
        final_date = start_date.replace(year=start_date.year + 1)
    else:
        final_date = None

    return final_date

def task_page(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    all_areas_in_specific_community = Area.objects.filter(community=community)
    all_seedbeds_in_specific_area = Seedbed.objects.filter(area__in=all_areas_in_specific_community)
    
    if request.method == "POST":
        description = request.POST.get('description')
        local = request.POST.get('local')
        recurrence = request.POST.get('recurrence')
        start_date = request.POST.get('start_date')
        start_date = timezone.datetime.strptime(start_date, "%Y-%m-%d").date()
        final_date = calculate_final_date(start_date, recurrence)
        materials = request.POST.get('materials')
        status = request.POST.get('status')
        responsible_users_raw = request.POST.get('responsible_users[]', '')
        responsible_users_ids = responsible_users_raw.split(',') if responsible_users_raw else []
        
        if start_date > final_date:
            messages.error(request, "A data final não pode ser antes da data inicial.")
            return redirect('task_page', community_id=community_id)

    
        responsible_users_ids = [int(id.strip()) for id in responsible_users_ids]
        
        if not description or not local or not start_date or not status or not responsible_users_ids:
            messages.error(request, 'Todos os campos são obrigatórios.')
        else:
            local_type = None
            local_id = None
            if local.startswith('area_'):
                local_type = 'area'
                local_id = local.replace('area_', '')
            elif local.startswith('seedbed_'):
                local_type = 'seedbed'
                local_id = local.replace('seedbed_', '')
            try:
                task = Task.objects.create(
                    community=community, 
                    materials=materials,
                    description=description,
                    local=local_type,
                    start_date=start_date,
                    final_date= final_date,
                    status=status,
                    recurrence=recurrence
                )

                if local_type == 'area':
                    task.area_id = int(local_id)
                elif local_type == 'seedbed':
                    task.seedbed_id = int(local_id)
                    seedbed = Seedbed.objects.get(id=int(local_id))
                    task.area_id = seedbed.area_id

                responsible_users = User.objects.filter(id__in=responsible_users_ids)
                task.responsible_users.set(responsible_users)

                task.save()
                messages.success(request, 'Tarefa criada com sucesso.')
                return redirect('task_page', community_id=community_id)
            except Exception as e:
                messages.error(request, f'Erro ao criar tarefa: {e}')


    tasks = Task.objects.filter(community=community) 
    membership_requests = MembershipRequest.objects.filter(community=community, status='pending')

    today = now().date() 
    for task in tasks:
        if task.final_date:
            days_left = (task.final_date - today).days
            task.days_left = days_left  
    
    context = {
        'tasks': tasks,
        'community': community,
        'all_areas': all_areas_in_specific_community,
        'all_seedbeds': all_seedbeds_in_specific_area,
        'status_choices': Task.STATUS_CHOICES,
        'recurrences': Task.RECURRENCE_CHOICES,
        'membership_requests' : membership_requests,
    }
    return render(request, 'tasks.html', context)

def delete_task(request, community_id, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    messages.success(request, "Tarefa excluída com sucesso.")
    return redirect('task_page', community_id=community_id)

def edit_task(request, community_id, task_id):
    task = get_object_or_404(Task, pk=task_id)

    # Verifica se a requisição é POST para atualizar a tarefa
    if request.method == 'POST':
        description = request.POST.get('description')
        materials = request.POST.get('materials')
        local = request.POST.get('local')
        start_date = request.POST.get('start_date')
        final_date = request.POST.get('final_date')
        status = request.POST.get('status')
        recurrence = request.POST.get('recurrence')
        responsible_users_raw = request.POST.getlist('responsible_users[]') 

        if not description or not local or not start_date or not status or not responsible_users_raw:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return redirect('task_page', community_id=community_id)

        try:
            responsible_users_ids = [int(user_id) for user_id in responsible_users_raw]

            # Validando se todos os IDs são válidos
            responsible_users = User.objects.filter(id__in=responsible_users_ids)
            if responsible_users.count() != len(responsible_users_ids):
                raise ValueError("Um ou mais IDs de responsáveis são inválidos.")

            # Lógica para identificar e processar o local (area ou seedbed)
            local_type = None
            local_id = None
            if local.startswith('area_'):
                local_type = 'area'
                local_id = local.replace('area_', '')
            elif local.startswith('seedbed_'):
                local_type = 'seedbed'
                local_id = local.replace('seedbed_', '')
            # Convertendo a start_date para formato de data
            start_date = timezone.datetime.strptime(start_date, "%Y-%m-%d").date()

            # Calculando a final_date com base na recorrência
            final_date = calculate_final_date(start_date, recurrence)


            task.materials = materials
            task.description = description
            task.local = local_type
            task.start_date = start_date
            task.final_date = final_date
            task.status = status
            task.recurrence = recurrence

            if local_type == 'area':
                task.area_id = int(local_id)
            elif local_type == 'seedbed':
                task.seedbed_id = int(local_id)
                seedbed = Seedbed.objects.get(id=int(local_id))
                task.area_id = seedbed.area_id

            # Atualizando os responsáveis pela tarefa
            task.responsible_users.set(responsible_users)

            task.save()
            messages.success(request, 'Tarefa atualizada com sucesso.')
            return redirect('task_page', community_id=community_id)

        except ValueError as e:
            messages.error(request, f'Erro de valor: {e}')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar tarefa: {e}')

        context = {
        'task': task,
        'community': Community.objects.get(id=community_id),
        'status_choices': Task.STATUS_CHOICES,
        'recurrences': Task.RECURRENCE_CHOICES,
        'responsible_user_ids': [user.id for user in task.responsible_users.all()],
        'all_seedbeds': Seedbed.objects.all(),
        'all_areas': Area.objects.all(),
    }

    return render(request, 'modal_edit_task.html', context)

