from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from .models import Area
from communities.models import Community
from seedbeds.models import Seedbed
from products.models import Product, TypeProduct
from django.contrib import messages

# View para listar as áreas
def area_manage(request, community_id):
    # Recupera a comunidade correspondente ao ID fornecido
    community = get_object_or_404(Community, id=community_id)
    
    # Recupera todas as áreas que pertencem à comunidade
    areas = community.areas.all()  # Usa o related_name 'areas' definido no modelo Area
    
    return render(request, 'area_manage.html', {'areas': areas, 'community': community})

# View para criar uma nova área
def area_create(request, community_id):
    # Recupera a comunidade correspondente ao ID fornecido
    community = get_object_or_404(Community, id=community_id)

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Verifica se já existe uma área com o mesmo nome na comunidade
        if Area.objects.filter(name=name, community=community).exists():
            messages.error(request, 'Uma área com esse nome já existe nesta comunidade. Por favor, escolha outro nome.')
            return render(request, 'area_create.html', {'community': community})  # Retorna ao formulário de criação com a mensagem de erro

        try:
            # Cria a nova área associada à comunidade
            area = Area.objects.create(
                name=name,
                description=description,
                community=community
            )
            messages.success(request, 'Área criada com sucesso.')
            return redirect('area_manage', community_id=community_id)  # Redireciona para a lista de áreas da comunidade
        
        except IntegrityError:
            messages.error(request, 'Erro ao criar a área. Tente novamente.')
            return render(request, 'area_create.html', {'community': community})  # Retorna ao formulário de criação com a mensagem de erro

    return render(request, 'area_create.html', {'community': community})

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
    
    return render(request, 'area_edit.html', {
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

    return render(request, 'area_delete.html', {'area': area})

def area_detail(request, community_id, area_id):
    community = get_object_or_404(Community, id=community_id)
    area = get_object_or_404(Area, id=area_id, community=community)
    
    # Recuperando os canteiros (seedbeds) associados à área
    seedbeds = Seedbed.objects.filter(area=area)

    context = {
        'community': community,
        'area': area,
        'seedbeds': seedbeds,  # Passando os canteiros para o template
    }
    return render(request, 'area_detail.html', context)