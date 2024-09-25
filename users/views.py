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
        name = request.POST.get('first_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        city = request.POST.get('city')
        state = request.POST.get('state')
        birthday = request.POST.get('birthday')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Esse usuário já existe.')
            return redirect('create_user')

        user = User.objects.create_user(
            first_name=name,
            username=username,
            email=email,
            password=password,
            city=city,
            state=state,
            birthday=birthday
        )
        user.save()
        messages.success(request, 'Usuário cadastrado com sucesso.')
        return HttpResponse('cadastrado')

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
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.cidade = request.POST.get('cidade')
        user.estado = request.POST.get('estado')
        user.data_nascimento = request.POST.get('data_nascimento')
        user.save()

        messages.success(request, 'Usuário editado com sucesso.')
        return redirect('get_all_users')

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('password')

        user = authenticate(username=username, password=senha)

        if user:
            login_django(request, user)
            messages.success(request, 'Autenticado com sucesso.')
            return HttpResponse('pagina de logado')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('login')

@login_required
def logout(request):
    logout_django(request)
    messages.success(request, 'Desconectado com sucesso.')
    return redirect('login')
