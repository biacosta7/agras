from django.shortcuts import render, redirect, get_object_or_404
from seedbeds.models import Seedbed
from communities.models import Community  
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def list_seedbeds(request):
    community = get_object_or_404(Community, id=request.user.community.id)  
    canteiros = Seedbed.objects.filter(community=community)  
    return render(request, 'list_seedbeds.html', {'canteiros': canteiros, 'community': community})

@login_required
def create_seedbed(request):
    user = request.user
    communities = user.communities_members.all()  # Obtém todas as comunidades do usuário

    if request.method == 'POST':
        # Supondo que você tenha um formulário que inclui a seleção da comunidade
        community_id = request.POST.get('community')  # O ID da comunidade selecionada
        community = Community.objects.get(id=community_id)

        # Criação do canteiro
        seedbed_name = request.POST.get('seedbed_name')
        Seedbed.objects.create(name=seedbed_name, community=community)

        return redirect('list-seedbeds')  # Redirecione para a lista de canteiros após a criação

    return render(request, 'create_seedbed.html', {'communities': communities})

@login_required
def edit_seedbed(request, seedbed_id):
    seedbed = get_object_or_404(Seedbed, id=seedbed_id)
    community = get_object_or_404(Community, id=request.user.community.id)  

    if request.method == 'POST':
        nome = request.POST.get('nome')  
        if nome:
            if Seedbed.objects.filter(nome=nome, community=community).exclude(id=seedbed_id).exists():
                messages.error(request, 'Já existe um canteiro com esse nome nesta comunidade. Por favor, tente novamente.')
                return render(request, 'list_seedbeds.html', {'canteiros': Seedbed.objects.filter(community=community), 'community': community}) 
            else:
                seedbed.nome = nome  
                seedbed.save()  
                messages.success(request, 'Canteiro editado com sucesso!')
                return redirect('list-seedbeds')  

    return render(request, 'list_seedbeds.html', {'canteiros': Seedbed.objects.filter(community=community), 'community': community})  

@login_required
def delete_seedbed(request, seedbed_id):
    seedbed = get_object_or_404(Seedbed, id=seedbed_id)  
    if request.method == 'POST':
        seedbed.delete() 
        messages.success(request, 'Canteiro deletado com sucesso!')
        return redirect('seedbeds:list-seedbeds') 
    return render(request, 'list_seedbeds.html', {'canteiros': Seedbed.objects.filter(community=request.user.community), 'community': request.user.community}) 