from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from areas.models import Area
from communities.models import Community, MembershipRequest, SendCommunityInvite
from users.models import User, FileUpload
from seedbeds.models import Seedbed
from django.utils import timezone
from django.http import HttpResponse
from django.db import IntegrityError

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
def send_community_invite(request, community_id, user_id):
    target_user = get_object_or_404(User, id=user_id)
    
    community = get_object_or_404(Community, id=community_id)
    print(community.id)
    if not community.admins.filter(id=request.user.id).exists():
        messages.error(request, 'Você não tem permissão para enviar convites nesta comunidade.')
        return redirect('manage_community', community.id)

    existing_invite = SendCommunityInvite.objects.filter(user=target_user, community=community, status='pending').first()

    if existing_invite and existing_invite.status == 'pending':
        messages.error(request, f'Já existe um convite para o usuário {target_user.username}')
        return redirect('manage_community', community.id)

    if existing_invite and existing_invite.status == 'rejected':
        existing_invite.delete()

    request_invite = MembershipRequest.objects.filter(user=target_user, community=community, status='pending').first()

    if request_invite and request_invite.status == 'pending':
        messages.info(request, f'Já existe uma solicitação de entrada do usuário {target_user.username}')
        return redirect('manage_community', community.id)

    if not existing_invite:
        SendCommunityInvite.objects.create(
            user=target_user,
            community=community,
            requested_by=request.user,
            status='pending',
            invite_date=timezone.now()
        )
        messages.info(request, 'Convite enviado com sucesso!')

    return redirect('manage_community', community.id)
@login_required
def accept_community_invite(request, invite_id):
    invite_request = get_object_or_404(SendCommunityInvite, id=invite_id)

    invite_request.status = 'approved'
    invite_request.decision_date = timezone.now()
    invite_request.save()

    invite_request.community.members.add(invite_request.user)

    messages.success(request, 'Solicitação aceita com sucesso!')
    return redirect('community_hub')


@login_required
def decline_community_invite(request, invite_id):
    invite_request = get_object_or_404(SendCommunityInvite, id=invite_id)

    invite_request.status = 'rejected'
    invite_request.decision_date = timezone.now()
    invite_request.save()

    messages.success(request, 'Solicitação recusada com sucesso!')
    return redirect('community_hub')

@login_required
def manage_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    all_users_not_in_your_community = User.objects.exclude(communities_members__id=community_id)
    
    membership_requests = MembershipRequest.objects.filter(community=community, status='pending')

    context = {
        'community': community,
        'membership_requests': membership_requests,
        'all_users': all_users_not_in_your_community
    }
    
    return render(request, 'manage_community.html', context)

@login_required
def kick_member(request, community_id, user_id):
    community = get_object_or_404(Community, id=community_id)
    user_to_be_kicked = get_object_or_404(User, id=user_id)

    if not community.admins.filter(id=request.user.id).exists():
        messages.error(request, 'Você não tem permissão para expulsar membros da comunidade.')
        return redirect('manage_community', community.id)
    
    if user_to_be_kicked == request.user:
        messages.error(request, 'Você não pode se expulsar da comunidade. Para sair vá em configurações.')
        return redirect('manage_community', community.id)
    
    if user_to_be_kicked == community.creator:
        messages.error(request, 'Você não pode expulsar o dono da comunidade.')
        return redirect('manage_community', community.id)
    
    community.members.remove(user_to_be_kicked)
    if community.admins.filter(id=request.user.id).exists():
        community.admins.remove(user_to_be_kicked)

    messages.success(request, f'Usuário {user_to_be_kicked.username} foi removido da comunidade com sucesso.')
    return redirect('manage_community', community.id)

@login_required
def promote_member(request, community_id, user_id):
    community = get_object_or_404(Community, id=community_id)
    user_to_be_admin = get_object_or_404(User, id=user_id)

    if community.admins.filter(id=request.user.id).exists():
        messages.error(request, f'O usuário {user_to_be_admin.username} já é administrador da comunidade.')
        return redirect('manage_community', community.id)
    
    if community.admins.filter(id=user_to_be_admin.id).exists():
        messages.error(request, f'O usuário {user_to_be_admin.username} já é administrador da comunidade.')
        return redirect('manage_community', community.id)
    
    community.admins.add(user_to_be_admin)
    messages.success(request, f'Usuário {user_to_be_admin.username} agora é administrador da comunidade.')
    return redirect('manage_community', community.id)

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

    membership_request.delete()

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

    membership_request.delete()

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
    invite_request = SendCommunityInvite.objects.filter(user=user, status='pending')

    context = {
        'communities': communities,
        'has_communities': has_communities,
        'user': user,
        'user_communities_count': user_communities_count,
        'invite_request': invite_request
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

def image_upload_view(request, user_id):
    image_url = None  # Variável para armazenar a URL da imagem
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']

        # Salvar o objeto no banco de dados
        new_image = FileUpload.objects.create(user=user,image=image)
        new_image.save()

        # Obter a URL da imagem para exibir
        image_url = new_image.image.url
        print(image_url)

    return render(request, 'upload.html', {'image_url': image_url})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Community

@login_required
def settings(request, community_id):
    community = get_object_or_404(Community, id=community_id)

    # Verificar permissões
    if request.user != community.creator and not community.admins.filter(id=request.user.id).exists():
        messages.error(request, 'Você não tem permissão para acessar as configurações dessa comunidade.')
        return redirect('community_hub')

    if request.method == "POST":
        action = request.POST.get('action')
        
        if action == "update":
            # Lógica para atualização da comunidade
            name = request.POST.get('name')
            description = request.POST.get('description')

            if Community.objects.filter(name=name).exclude(pk=community_id).exists():
                messages.error(request, 'Já existe uma comunidade com esse nome.')
                return render(request, 'settings.html', {'community': community})

            community.name = name
            community.description = description
            community.save()
            messages.success(request, 'Comunidade editada com sucesso.')

        elif action == "delete":
            # Lógica para exclusão da comunidade
            community.delete()
            messages.success(request, 'Comunidade deletada com sucesso.')
            return redirect('community_hub')

    return render(request, 'settings.html', {'community': community})

@login_required
def profile(request, community_id):
    # Obtém a comunidade pelo ID, ou retorna 404 se não existir
    community = get_object_or_404(Community, id=community_id)

    # Verifica se o usuário é membro da comunidade
    if not community.members.filter(id=request.user.id).exists():
        messages.error(request, 'Você não tem acesso a esta comunidade.')
        return redirect('community_hub')

    # Usuário autenticado
    user = request.user

    if request.method == "POST":
        # Processa a atualização de informações do perfil
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        state = request.POST.get('state')

        # Validação de dados
        valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
        if not set(username).issubset(valid_chars):
            messages.error(request, 'O nome de usuário deve conter apenas letras, números ou underlines.')
            return redirect('profile', community_id=community.id)

        valid_name = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ")
        if not set(first_name).issubset(valid_name):
            messages.error(request, 'O nome não deve conter números ou caracteres especiais.')
            return redirect('profile', community_id=community.id)

        if '@' not in email or email.count('@') != 1:
            messages.error(request, 'Por favor, insira um email válido.')
            return redirect('profile', community_id=community.id)

        if User.objects.filter(username=username).exclude(id=user.id).exists():
            messages.error(request, 'Este nome de usuário já está em uso.')
            return redirect('profile', community_id=community.id)

        if User.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, 'Já existe um usuário com este email.')
            return redirect('profile', community_id=community.id)

        # Atualiza as informações do usuário
        user.first_name = first_name
        user.username = username
        user.email = email
        user.phone = phone
        user.city = city
        user.state = state

        try:
            user.save()
            messages.success(request, 'Credenciais atualizadas com sucesso.')
        except IntegrityError:
            messages.error(request, 'Erro ao atualizar as credenciais. Tente novamente.')
            return redirect('profile', community_id=community.id)

    # Renderiza o template com as informações do usuário e da comunidade
    return render(request, 'myprofile.html', {'user': user, 'community': community})
