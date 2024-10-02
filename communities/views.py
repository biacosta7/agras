from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Community
from users.models import User

@login_required
def home_view(request):
    return redirect('community_hub')

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

        members_ids = request.POST.getlist('members')
        members = User.objects.filter(id__in=members_ids)
        community.members.set(members)

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

    if request.user != community.creator and not community.admins.filter(id=request.user.id).exists():
        messages.error(request, 'Você não tem permissão para excluir essa comunidade.')
        return redirect('community_hub')

    community.delete()
    messages.success(request, 'Comunidade deletada com sucesso.')
    return redirect('community_hub')