from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from .models import ChatBot
from django.http import HttpResponseRedirect, JsonResponse
import google.generativeai as genai
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
import json

# Configura a API do Gemini com a chave de API
genai.configure(api_key=os.environ["API_KEY"])

@csrf_protect
@login_required
def ask_question(request, community_id, user_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get('text', '')

            # Inicializa o modelo de IA e inicia o chat
            model = genai.GenerativeModel("gemini-pro")
            chat = model.start_chat()
            
            # Envia a pergunta para a IA e recebe a resposta
            response = chat.send_message(text)
            user = request.user
            
            # Salva a interação no banco de dados
            ChatBot.objects.create(text_input=text, gemini_output=response.text, user=user)

            response_data = {
                "text": response.text,
            }

            return JsonResponse({"data": response_data})
        except Exception as e:
            # Log de erro
            print(f"Error processing request: {e}")
            return JsonResponse({"error": "An error occurred while processing your request."}, status=500)
    else:
        return HttpResponseRedirect(
            reverse("chat", args=[community_id, user_id])
        )

@login_required
def chat(request, community_id, user_id):
    user = request.user
    
    # Filtra as interações do usuário atual
    chats = ChatBot.objects.filter(user=user)
    
    # Renderiza o template com o histórico de chat e os IDs
    return render(request, "chat_bot.html", {
        "chats": chats,
        "community_id": community_id,
        "user_id": user_id
    })

