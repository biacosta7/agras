from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from areas.models import Area
from communities.models import Community, MembershipRequest
from seedbeds.models import Seedbed
from django.utils import timezone
from .models import ImageUpload
from django.http import HttpResponse
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
import os

@login_required
def home_view(request):
    return redirect('community_hub')

@login_required
def dashboard_view(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    
    # Verificação se o usuário é membro ou administrador da comunidade
    if request.user not in community.members.all() and request.user not in community.admins.all():
        existing_request = MembershipRequest.objects.filter(user=request.user, community=community).first()

        if existing_request and existing_request.status == 'rejected':
            existing_request.delete()
            created = True
        elif existing_request:
            messages.info(request, 'Você já enviou uma solicitação para esta comunidade. Aguarde a resposta do administrador.')
            return redirect('community_hub')

        if not existing_request or created:
            MembershipRequest.objects.create(
                user=request.user,
                community=community,
                status='pending',
                request_date=timezone.now()
            )
            messages.info(request, 'Sua solicitação para entrar na comunidade foi enviada ao administrador.')
            
        return redirect('community_hub')

    areas = Area.objects.filter(community=community)
    seedbeds = Seedbed.objects.filter(area__community=community)
    membership_requests = MembershipRequest.objects.filter(community=community, status='pending')
    users = community.members.all().union(community.admins.all()) if community else None

    context = {
        'community': community,
        'areas': areas,
        'seedbeds': seedbeds,
        'membership_requests': membership_requests,
        'users': users
    }

    return render(request, 'dashboard.html', context)

@login_required
def manage_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    
    # Verifica se o usuário tem permissão para acessar o gerenciamento
    if request.user != community.creator and not community.admins.filter(id=request.user.id).exists():
        messages.error(request, 'Você não tem permissão para gerenciar esta comunidade.')
        return redirect('community_hub')
    
    membership_requests = MembershipRequest.objects.filter(community=community, status='pending')

    context = {
        'community': community,
        'membership_requests': membership_requests,
    }
    
    return render(request, 'manage_community.html', context)

@login_required
def aceitar_solicitacao(request, request_id):
    membership_request = get_object_or_404(MembershipRequest, id=request_id)

    if request.user != membership_request.community.creator and not membership_request.community.admins.filter(id=request.user.id).exists():
        messages.error(request, 'Você não tem permissão para aceitar esta solicitação.')
        return redirect('manage_community', community_id=membership_request.community.id)

    membership_request.status = 'approved'
    membership_request.decision_date = timezone.now()
    membership_request.save()

    membership_request.community.members.add(membership_request.user)

    messages.success(request, 'Solicitação aceita com sucesso!')
    return redirect('manage_community', community_id=membership_request.community.id)

@login_required
def rejeitar_solicitacao(request, request_id):
    membership_request = get_object_or_404(MembershipRequest, id=request_id)

    if request.user != membership_request.community.creator and not membership_request.community.admins.filter(id=request.user.id).exists():
        messages.error(request, 'Você não tem permissão para rejeitar esta solicitação.')
        return redirect('manage_community', community_id=membership_request.community.id)

    membership_request.status = 'rejected'
    membership_request.decision_date = timezone.now()
    membership_request.save()

    messages.success(request, 'Solicitação rejeitada com sucesso!')
    return redirect('manage_community', community_id=membership_request.community.id)

@login_required
def community_list(request):
    user = request.user
    user_communities = user.communities_members.all()
    is_admin_of_community = user.admin_communities.exists()
    has_communities = user_communities.exists() or is_admin_of_community
    communities = Community.objects.all()
    user_communities_count = request.user.communities_members.count() + request.user.admin_communities.count()

    context = {
        'communities': communities,
        'has_communities': has_communities,
        'user': user,
        'user_communities_count': user_communities_count
    }

    return render(request, 'hub.html', context)

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
        community.members.add(creator)
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

@login_required
def list_members(request, community_id):
    community = get_object_or_404(Community, id=community_id)

    members = community.members.all()

    context = {
        'community': community,
        'members': members,
    }

    return render(request, 'list_members.html', context)

def generate_sas_url(blob_name):
    account_name = os.getenv('AZURE_ACCOUNT_NAME')
    account_key = os.getenv('AZURE_ACCOUNT_KEY')
    container_name = os.getenv('AZURE_CONTAINER', 'media')
    current_time = timezone.now()

    sas_token = generate_blob_sas(
        account_name=account_name,
        account_key=account_key,
        container_name=container_name,
        blob_name=blob_name,
        permission=BlobSasPermissions(read=True),
        expiry=current_time + timedelta(hours=1)  # Define a validade da URL
    )

    url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
    return url

def image_upload_view(request):
    image_url = None
    if request.method == 'POST' and request.FILES.get('image'):
        title = request.POST.get('title', 'Untitled')
        image = request.FILES['image']

        # Salvar o objeto no banco de dados
        new_image = ImageUpload.objects.create(title=title, image=image)
        new_image.save()

        # Gerar a URL SAS para a imagem
        image_url = generate_sas_url(new_image.image.name)

    return render(request, 'upload.html', {'image_url': image_url})
