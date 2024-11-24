from .models import ChatBot
from products.models import TypeProduct
import requests

def chat_messages(request):
    if request.user.is_authenticated:
        chats = ChatBot.objects.filter(user=request.user).order_by('-date')[:10]
        
        # Obter IDs
        community_id = request.resolver_match.kwargs.get('community_id', None)
        user_id = request.user.id  # ID do usuário autenticado
        user_name = getattr(request.user, 'name', request.user.username)  # Usa o campo 'name', ou 'username' como fallback

        # Produtos da comunidade
        products = []
        if community_id:
            products = TypeProduct.objects.filter(community_id=community_id).values_list('name', flat=True)
        
        return {
            'chats': chats,
            'community_id': community_id,
            'user_id': user_id,
            'user_name': user_name,
            'location': 'Pernamuco',
            'type_products': list(products),
            'interests': 'agricultura',
        }
    return {}
