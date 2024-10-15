from django.shortcuts import render, redirect, get_object_or_404
from seedbeds.models import Seedbed
from communities.models import Community  
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def list_seedbeds(request, community_id):
    community = get_object_or_404(Community, id=community_id)  
    canteiros = Seedbed.objects.filter(community=community)  
    return render(request, 'list_seedbeds.html', {'canteiros': canteiros, 'community': community})

@login_required
def create_seedbed(request, community_id):
    user = request.user
    communities = user.communities_members.all()  # Obtém todas as comunidades do usuário

    # Obter a comunidade específica selecionada
    community = get_object_or_404(Community, id=community_id)

    if request.method == 'POST':
        # Obter o nome do canteiro
        seedbed_name = request.POST.get('seedbed_name')  # Certifique-se de que este campo está no formulário
        
        if seedbed_name:
            # Criação do canteiro
            Seedbed.objects.create(nome=seedbed_name, community=community)
            messages.success(request, 'Canteiro criado com sucesso!')
            return redirect('seedbeds:list_seedbeds', community_id=community.id)  # Redirecionar para a lista de canteiros da comunidade
        else:
            messages.error(request, 'Por favor, insira um nome válido para o canteiro.')
    
    context = {
        'communities': communities,
        'community': community,
    }
    return render(request, 'create_seedbed.html', context)

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
                return redirect('list_seedbeds')  

    return render(request, 'list_seedbeds.html', {'canteiros': Seedbed.objects.filter(community=community), 'community': community})  

@login_required
def delete_seedbed(request, community_id, seedbed_id):
    # Buscando o canteiro e a comunidade correspondente
    seedbed = get_object_or_404(Seedbed, id=seedbed_id, community_id=community_id)
    community = get_object_or_404(Community, id=community_id)

    if request.method == 'POST':
        seedbed.delete()  # Deletando o canteiro
        messages.success(request, 'Canteiro deletado com sucesso!')
        # Redirecionando para a lista de canteiros, passando o ID da comunidade
        return redirect('seedbeds:list_seedbeds', community_id=community_id)
    
    # Caso não seja POST, renderizar uma página de confirmação
    context = {
        'seedbed': seedbed,
        'community': community,
    }
    
    return render(request, 'confirm_delete.html', context)