from .models import ChatBot
from products.models import TypeProduct
import requests
import json
from django.utils.safestring import mark_safe
from django.core.serializers.json import DjangoJSONEncoder


def chat_messages(request):
    if request.user.is_authenticated:
        chats = ChatBot.objects.filter(user=request.user).order_by('-date')[:10]

        # Serializar o queryset para JSON
        serialized_chats = json.dumps(
            list(chats.values('id', 'text_input', 'gemini_output', 'date')),
            ensure_ascii=False,
            cls=DjangoJSONEncoder  # Lidando com datetime automaticamente
        )
        
        # Obter IDs
        community_id = request.resolver_match.kwargs.get('community_id', None)
        user_id = request.user.id  # ID do usuário autenticado
        user_name = getattr(request.user, 'name', request.user.username)  # Usa o campo 'name', ou 'username' como fallback

        type_products = TypeProduct.objects.filter(community=community_id)

        organisms = [
            "Colchonilas",
            "Joaninhas"
            "Cupins",
            "Pulgões",
            "Moscas",
            "Percevejo",
            "Lagarta",
            "Ácaro"
        ]

        # Produtos da comunidade
        products = []
        if community_id:
            products = TypeProduct.objects.filter(community_id=community_id).values_list('name', flat=True)
        
        return {
            'chats': mark_safe(serialized_chats),
            'community_id': community_id,
            'user_id': user_id,
            'user_name': user_name,
            'location': 'Pernamuco',
            'products': list(products),
            'interests': 'agricultura',
            'type_products': type_products,
            'organisms': organisms,
        }
    return {}
