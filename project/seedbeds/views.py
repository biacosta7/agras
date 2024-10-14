from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from seedbeds.models import Seedbed
from products.models import Product
from django.contrib import messages

def list_seedbeds(request):
    # Obtém todos os canteiros
    canteiros = Seedbed.objects.all()  # Busca todos os canteiros
    return render(request, 'list_seedbeds.html', {'canteiros': canteiros})

def create_seedbed(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')  # Obtém o nome do Seedbed a partir do request
        if nome:
            if Seedbed.objects.filter(nome=nome).exists():
                return render(request, 'create_seedbed.html', {
                    'error_message': 'Já existe um canteiro com esse nome.',
                })
            else:
                Seedbed.objects.create(nome=nome)  
                return redirect('seedbeds:list-seedbeds') 
    return render(request, 'create_seedbed.html')  # Renderiza o formulário vazio se não for POST

def delete_seedbed(request, seedbed_id):
    seedbed = get_object_or_404(Seedbed, id=seedbed_id)  # Obtém o Seedbed com base no ID
    if request.method == 'POST':
        seedbed.delete()  # Deleta o Seedbed
        messages.success(request, 'Canteiro deletado com sucesso!')
        return redirect('seedbeds:list-seedbeds')  # Redireciona para a lista de Seedbeds


    return render(request, 'confirm_delete.html', {'seedbed': seedbed})