from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Community

@login_required
def home_view(request):
    return redirect('community_hub')

@login_required
def dashboard_view(request):
    community_id = request.GET.get('community_id')  # Captura o ID da comunidade a partir da URL
    community = get_object_or_404(Community, id=community_id)

    # Verificação se o usuário é membro ou administrador da comunidade
    if request.user not in community.members.all() and request.user not in community.admins.all():
        messages.error(request, 'Você não tem permissão para acessar o dashboard desta comunidade.')
        return redirect('community_hub')

    # Recuperando os plantios e canteiros associados à comunidade
    products = Product.objects.filter(community=community)
    seedbeds = community.seedbeds.all()  # Certifique-se de que você está acessando os canteiros corretamente

    context = {
        'community': community,
        'products': products,
        'seedbeds': seedbeds,
    }

    return render(request, 'dashboard.html', context)

@login_required
def community_list(request):
    communities = Community.objects.all()
    return render(request, 'hub.html', {'communities': communities})

@login_required
def create_community(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        creator = request.user

        if Community.objects.filter(name=name).exists():
            messages.error(request, 'Já existe uma comunidade com esse nome.')
            return redirect('community_hub')

        community = Community.objects.create(
            name=name,
            description=description,
            creator=creator
        )

        community.admins.add(creator)

        messages.success(request, 'Comunidade cadastrada com sucesso.')
        return redirect('community_hub')

    return redirect('community_hub')

@login_required
def update_community(request, pk):
    community = get_object_or_404(Community, pk=pk)

    if request.user != community.creator and not community.admins.filter(id=request.user.id).exists():
        messages.error(request, 'Você não tem permissão para editar essa comunidade.')
        return redirect('community_hub')

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        if Community.objects.filter(name=name).exclude(pk=pk).exists():
            messages.error(request, 'Já existe uma comunidade com esse nome.')
            return render(request, 'community_hub', {'community': community})

        community.name = name
        community.description = description
        community.save()

        messages.success(request, 'Comunidade editada com sucesso.')
        return redirect('community_hub') 

    return render(request, 'community_hub', {'community': community})

@login_required
def delete_community(request, pk):
    community = get_object_or_404(Community, pk=pk)

    # Verificação de permissões: o usuário deve ser o criador ou um administrador
    if request.user != community.creator and not community.admins.filter(id=request.user.id).exists():
        messages.error(request, 'Você não tem permissão para excluir essa comunidade.')
        return redirect('community_hub')

    community.delete()
    messages.success(request, 'Comunidade deletada com sucesso.')
    return redirect('community_hub')

def community_detail(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    return render(request, 'community_detail.html', {'community': community})