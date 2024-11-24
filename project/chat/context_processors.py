from .models import ChatBot

def chat_messages(request):
    if request.user.is_authenticated:
        chats = ChatBot.objects.filter(user=request.user).order_by('-date')[:10]
        
        # Obter IDs
        community_id = request.resolver_match.kwargs.get('community_id', None)
        user_id = request.user.id  # ID do usuário autenticado
        
        return {
            'chats': chats,
            'community_id': community_id,
            'user_id': user_id,
        }
    return {}
