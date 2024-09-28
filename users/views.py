from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as login_django, logout as logout_django
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib import messages

def create_user(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        city = request.POST.get('city')
        state = request.POST.get('state')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Esse usuário já existe.')
            return redirect('create_user')
        if password == confirm_password:
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
            return HttpResponse('cadastrado')
        else:
            messages.error(request, 'Senhas não coincidem.')
            return redirect('create_user')


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

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "GET":
        return render(request, 'edit_user.html', {'user': user})
    else:
        user.first_name = request.POST.get('firts_name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.city = request.POST.get('city')
        user.state = request.POST.get('state')
        user.save()

        messages.success(request, 'Usuário editado com sucesso.')
        return redirect('get_all_users')

def login(request):
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

            return HttpResponse('pagina de logado')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('login')

@login_required
def logout(request):
    logout_django(request)
    messages.success(request, 'Desconectado com sucesso.')
    return redirect('login')
