from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, TypeProduct
from django.contrib import messages
from django.core.exceptions import ValidationError
from communities.models import Community

@login_required  
def create_product_view(request, community_id):
    community = get_object_or_404(Community, id=community_id)

    if request.method == 'POST':
        type_name = request.POST.get('tipo_nome')
        quantity = request.POST.get('quantidade')
        planting_date = request.POST.get('data_plantio')

        # Verificando se o tipo de produto existe na comunidade correta
        type_product = get_object_or_404(TypeProduct, name=type_name, community=community)

        errors = []

        # Validação dos campos
        if not type_name:
            errors.append("O campo 'Cultivo' é obrigatório.")
        if not planting_date:
            errors.append("O campo 'Data de plantio' é obrigatório.")
        if not quantity:
            errors.append("O campo 'Quantidade' é obrigatório.")
        
        if errors:
            return render(request, 'create_product.html', {
                'errors': errors,
                'community': community,
                'tipos_produtos': TypeProduct.objects.filter(community=community)  # Filtrando por comunidade
            })

        try:
            # Criando o produto associado à comunidade
            product = Product.objects.create(
                type_product=type_product,  # Alterado para 'type_product'
                seedbed=None,  # Ou defina um seedbed apropriado, se necessário
                community=community,
                quantity=int(quantity),
                planting_date=planting_date
            )
            product.full_clean()  
            product.save()
            
            messages.success(request, f'Produto {product.nome_type_product} cadastrado com sucesso na comunidade {community.name}.')

        except ValidationError as e:
            messages.error(request, f"Erro de validação: {e}")

        return redirect('dashboard', community.id)

    # Filtrando tipos de produtos por comunidade
    tipos_produtos = TypeProduct.objects.filter(community=community)
    return render(request, 'create_product.html', {'community': community, 'tipos_produtos': tipos_produtos})

@login_required  
def create_typeproduct_view(request, community_id):
    community = get_object_or_404(Community, id=community_id)

    if request.method == 'POST':
        nome = request.POST.get('nome').capitalize()
        
        # Verificando se o tipo de produto já existe na mesma comunidade
        if TypeProduct.objects.filter(name=nome, community=community).exists():
            messages.error(request, f'O cultivo {nome} já existe na comunidade {community.name}. Por favor, escolha um nome diferente.')
            return render(request, 'create_typeproduct.html', {'community': community})

        typeproduct = TypeProduct.objects.create(
            name=nome,
            community=community  # Associando o tipo de produto à comunidade
        )

        messages.success(request, f'Novo cultivo {typeproduct.name} criado com sucesso na comunidade {community.name}.')
        return redirect(f'/comunidades/dashboard/?community_id={community.id}')

    return render(request, 'create_typeproduct.html', {'community': community})