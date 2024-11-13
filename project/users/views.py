from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as login_django, logout as logout_django
from django.contrib.auth.decorators import login_required
from .models import User
from communities.models import Community
from django.contrib import messages

def create_user(request):
    if request.method == "GET":
        return render(request, 'signup.html')
    else:
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        city = request.POST.get('city')
        state = request.POST.get('state')
        confirm_password = request.POST.get('confirm_password')

        form_data = {
            'first_name': first_name,
            'username': username,
            'email': email,
            'city': city,
            'state': state,
        }

        valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
        if not set(username).issubset(valid_chars):
            messages.error(request, 'O nome de usuário deve conter apenas letras, números ou underlines, sem espaços ou caracteres especiais')
            return render(request, 'signup.html', form_data)

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Esse usuário já existe.')
            return render(request, 'signup.html', form_data)

        valid_name = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        if not set(first_name).issubset(valid_name):
            messages.error(request, 'O nome não deve conter números ou caracteres especiais')
            return render(request, 'signup.html', form_data)

        if ' ' in password:
            messages.error(request, 'A senha não pode conter espaços.')
            return render(request, 'signup.html', form_data)

        if password.isdigit():
            messages.error(request, 'A senha não pode ser composta apenas por números.')
            return render(request, 'signup.html', form_data)

        if '@' not in email or email.count('@') != 1:
            messages.error(request, 'Por favor, insira um email válido')
            return render(request, 'signup.html', form_data)

        if password == confirm_password:
            try:
                user = User.objects.create_user(
                    first_name=first_name,
                    username=username,
                    email=email,
                    password=password,
                    city=city,
                    state=state,
                )
                user.save()
                messages.success(request, 'Usuário cadastrado com sucesso.')
                return redirect('login')
            except IntegrityError:
                messages.error(request, 'Já existe um usuário com este email. Tente novamente.')
                return render(request, 'signup.html', form_data)
        else:
            messages.error(request, 'Senhas não coincidem.')
            return render(request, 'signup.html', form_data)

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'Usuário deletado com sucesso.')
    return redirect('get_all_users')


@login_required
def get_all_users(request):
    users = User.objects.all()
    return render(request, 'listar_usuarios.html', {'users': users})

def login(request):
    if request.user.is_authenticated:
        return redirect('community_hub')
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        login_input = request.POST.get('login_input')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember')

        user = authenticate(username=login_input, password=password)

        if user is None:
            try:
                user = User.objects.get(email=login_input)
                user = authenticate(username=user.username, password=password)
            except User.DoesNotExist:
                user = None

        if user:
            login_django(request, user)
            messages.success(request, 'Autenticado com sucesso.')
            
            if remember_me: 
                request.session.set_expiry(None)  
            else:
                request.session.set_expiry(0) 

            return redirect('community_hub')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('login')

@login_required
def logout(request):
    logout_django(request)
    messages.success(request, 'Desconectado com sucesso.')
    return redirect('login')

def forgot_password(request):
    if request.method == "GET":
        return render(request, 'forgot_password.html')
    else: 
        login_input = request.POST.get('login_input')
        new_password = request.POST.get('password')
        confirm_new_password = request.POST.get('confirm_password')

        form_login_input = {
            'login_input': login_input
        }

        if new_password == confirm_new_password:
            
            if ' ' in new_password:
                messages.error(request, 'A senha não pode conter espaços.')
                return render(request, 'forgot_password.html', form_login_input)

            if new_password.isdigit():
                messages.error(request, 'A senha não pode ser composta apenas por números.')
                return render(request, 'forgot_password.html', form_login_input)
            
            try:
                user = User.objects.get(username=login_input) if User.objects.filter(username=login_input).exists() else User.objects.get(email=login_input)

                user.set_password(new_password)
                user.save()
                messages.success(request, 'Senha redefinida com sucesso.')
                return redirect('login')

            except User.DoesNotExist:
                messages.error(request, 'Usuário não encontrado.')
                return redirect('forgot_password')
        else:
            messages.error(request, 'As senhas não coincidem.')
            return redirect('forgot_password')
        
        
@login_required
def update_user(request):
    user = request.user
    community = None

    # Verifica se o usuário está em alguma comunidade, pegando a primeira comunidade associada a ele
    if user.communities_members.exists():
        # Se o usuário está em uma comunidade, pegamos a primeira comunidade
        community = user.communities_members.first()

    if request.method == "GET":
        # Passa o contexto de 'community' para o template se houver
        return render(request, 'edit_profile.html', {'user': user, 'community': community})
    
    else:
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        city = request.POST.get('city')
        state = request.POST.get('state')

        # Validação dos dados recebidos
        valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
        if not set(username).issubset(valid_chars):
            messages.error(request, 'O nome de usuário deve conter apenas letras, números ou underlines, sem espaços ou caracteres especiais.')
            return redirect('edit')

        valid_name = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        if not set(first_name).issubset(valid_name):
            messages.error(request, 'O nome não deve conter números ou caracteres especiais.')
            return redirect('edit')

        if '@' not in email or email.count('@') != 1:
            messages.error(request, 'Por favor, insira um email válido.')
            return redirect('edit')

        if User.objects.filter(username=username).exclude(id=user.id).exists():
            messages.error(request, 'Este nome de usuário já está em uso.')
            return redirect('edit')

        if User.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, 'Já existe um usuário com este email.')
            return redirect('edit')

        # Atualiza as credenciais do usuário
        user.first_name = first_name
        user.username = username
        user.email = email
        user.city = city
        user.state = state

        try:
            user.save()
            messages.success(request, 'Credenciais atualizadas com sucesso.')
        except IntegrityError:
            messages.error(request, 'Erro ao atualizar as credenciais. Tente novamente.')
            return redirect('edit')

        return render(request, 'login.html', {'community': community})
