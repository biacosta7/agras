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
            user_context = data.get('user_context', {})

            # Construir o prompt personalizado
            prompt = (
                f"Usuário: {user_context.get('user_name').title()}.\n"
                f"Condições climáticas: {user_context.get('climate')}.\n"
                f"Localização: {user_context.get('location')}.\n"
                f"Produtos cadastrados: {', '.join(user_context.get('type_products', []))}.\n"
                f"Interesses: {user_context.get('interests')}.\n\n"
                f"Pergunta: {text}"
            )

            # IA responde ao prompt
            model = genai.GenerativeModel("gemini-pro")
            chat = model.start_chat()
            response = chat.send_message(prompt)

            # Salvar interação no banco de dados
            ChatBot.objects.create(
                text_input=text,
                gemini_output=response.text,
                user=request.user
            )

            return JsonResponse({"data": {"text": response.text}})
        except Exception as e:
            print(f"Error processing request: {e}")
            return JsonResponse({"error": "An error occurred while processing your request."}, status=500)
    else:
        return HttpResponseRedirect(reverse("chat", args=[community_id, user_id]))

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

