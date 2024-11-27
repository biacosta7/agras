from django.shortcuts import get_object_or_404, render, reverse
from django.contrib.auth.decorators import login_required
from products.models import TypeProduct
from .models import ChatBot
from django.http import HttpResponseRedirect, JsonResponse
import google.generativeai as genai
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
import json
from django.core.cache import cache

# Configura a API do Gemini com a chave de API
genai.configure(api_key=os.environ["API_KEY"])

# Extrair cultivos selecionados da pergunta atual
def extract_selected_crops(text):
    if text.startswith("User: Cultivos selecionados: "):
        crops = text.replace("User: Cultivos selecionados: ", "User: Cultivos selecionado anteriormente:").strip()
        if crops:
            # Remove cultivos duplicados
            crops_list = crops.split(",")  # Supondo que os cultivos sejam separados por vírgulas
            unique_crops = set(crops_list)  # Remove duplicados
            return ", ".join(sorted(unique_crops))  # Retorna os cultivos únicos, separados por vírgula e ordenados
    elif text.startswith("Chat IA: Cultivos selecionados: "):
        crops = text.replace("Chat IA: **Cultivos selecionados:**", "").strip()
        if crops:
            # Remove cultivos duplicados
            crops_list = crops.split(",")  # Supondo que os cultivos sejam separados por vírgulas
            unique_crops = set(crops_list)  # Remove duplicados
            return ", ".join(sorted(unique_crops))  # Retorna os cultivos únicos, separados por vírgula e ordenados
    return None

@csrf_protect
@login_required
def ask_question(request, community_id, user_id):
    if request.method == "POST":
        try:
            # Obtém os dados da requisição
            data = json.loads(request.body)
            text = data.get('text', '')
            user_context = data.get('user_context', {})

            # Obtém os cultivos selecionados
            type_products = TypeProduct.objects.filter(community=community_id).values_list('name', flat=True)

            # Verificar se a resposta já está em cache
            cached_response = cache.get(f"response_{text}_{user_id}")
            if cached_response:
                return JsonResponse({"data": {"text": cached_response}})

            # Recuperar o histórico de interações do usuário / Limitar o número de interações para as últimas 10
            chat_history = ChatBot.objects.filter(user=request.user).order_by('date')[:10]
            
            # Construir o histórico de conversas no formato adequado para o prompt
            history_text = ""
            for chat in chat_history:
                history_text += f"User: {chat.text_input}\n"
                history_text += f"Chat IA: {chat.gemini_output}\n"
            
            # Cultivos selecionados na pergunta atual
            current_crops = extract_selected_crops(history_text)

            print(text)
            
            # Construir o prompt com o histórico
            prompt = (
                f"Pergunta: {text}\n"
                f"\nHistórico de conversa:\n[{current_crops}]\n"
                f"\nGuia:\n"
                f"1. Se meu nome não for 'None', me chame pelo meu nome (com letras iniciais maiúsculas). Meu nome: {user_context.get('user_name')}.\n"
                f"2. Seu nome é Chat IA e você é o assistente virtual impulsionado por inteligência artificial do AGRAS.\n"
                f"3. Se houver cultivos selecionados na 'Pergunta', forneça utilidades, saberes populares ou dicas sobre esses cultivos: {current_crops}. Caso contrário, fale sobre como você pode me ajudar no meu contexto agrícola.\n"
                f"4. Divida as respostas longas em parágrafos menores para facilitar a leitura.\n"
                f"5. Não mencione a inexistência de cultivos selecionados nem informações que você não tem. Baseie suas respostas nas informações fornecidas.\n"
                f"6. Para selecionar cultivos, clique em 'Utilidades' na parte superior.\n"
                f"7. Para selecionar organismos indesejados, clique em 'Organismos', na parte superior.\n"
                f"8. Na primeira interação, se não for uma saudação, seja direto e evite grandes textos. Se for uma saudação, seja breve e pergunte como posso ajudar.\n"
                f"9. Se a 'Pergunta' for apenas: 'Cultivos selecionados: (lista não vazia)', responda com utilidades ou saberes populares sobre os cultivos, sem saudações.\n"
                f"10. Verifique apenas se há cultivos selecionados na pergunta atual (mais recente), ignore os cultivos selecionados anteriormente no 'Histórico de conversa'.\n"
                f"11. Sugestões de cultivos é diferente de cultivos selecionados.\n"
                f"12. Caso não haja informações suficientes nas instruções para responder a pergunta, use suas próprias fontes\n"
                f"\nContextos:\n"
                f"Clima: {user_context.get('climate')}\n"
                f"Sugestões de cultivos: {', '.join(list(type_products))}\n"
                f"Interesses: Agricultura\n\n"
            )

            print(prompt)

            # IA responde ao prompt
            model = genai.GenerativeModel("gemini-pro")
            chat = model.start_chat()
            response = chat.send_message(prompt)

            # Armazenar a resposta no cache por um tempo (60 minutos)
            cache.set(f"response_{text}_{user_id}", response.text, timeout=3600)

            # Salvar interação no banco de dados
            ChatBot.objects.create(
                text_input=text,
                gemini_output=response.text,
                user=request.user
            )

            return JsonResponse({"data": {"text": response.text}})
        except Exception as e:
            print(f"Error processing request: {e}")
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
    else:
        return HttpResponseRedirect(reverse("chat", args=[community_id, user_id]))


# Função abaixo não está sendo usada, era do html do chatbot
@login_required
def chat(request, community_id, user_id):
    user = request.user
    
    # Filtra as interações do usuário atual
    chats = ChatBot.objects.filter(user=user)

    # Renderiza o template com o histórico de chat e os IDs
    return render(request, "chat_bot.html", {
        "chats": chats,
        "community_id": community_id,
        "user_id": user_id,
    })
