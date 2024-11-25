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

            # Obtém os cultivos selecionados
            type_products = TypeProduct.objects.filter(community=community_id).values_list('name', flat=True)

            # Construir o prompt
            prompt = (
                f"Pergunta: {text}\n"
                f"Se meu nome não for 'None', me chame pelo meu nome (com letras iniciais maiúsculas): {user_context.get('user_name')}.\n"
                f"Condições climáticas: {user_context.get('climate')}.\n"
                #f"Localização: {user_context.get('location')}.\n"
                f"Cultivos da comunidade: {', '.join(list(type_products))}.\n"
                f"Interesses: {user_context.get('interests')}.\n\n"
                f"Por favor, se houver cultivos selecionados, forneça utilidades, saberes populares ou dicas sobre os cultivos selecionados. Caso contrário, fale sobre as outras coisas, como como você pode me ajudar no meu contexto de agricultura.\n"
                f"Tente não fazer grandes parágrafos, reparta, se possível, os textos, para uma leitura mais fluída quando tiver muitas informações de fato necessárias.\n"
                f"Não mencione a inexistência de cultivos selecionados, nem as informações que você não possui, tente me ajudar com as informacoes que eu te passei.\n"
                f"Para eu selecionar cultivos, devo clicar em 'Utilizades' localizado acima."
                f"Na primeira interação, apenas se não for uma saudação, não faça grandes textos. Se eu só te der uma saldação, seja breve e educado, perguntando o que desejo e como você pode me ajudar.\n"
                f"Mesmo que seja a primeira interação, se a pergunta for apenas: 'Cultivos selecionados: (lista de cultivos não vazia aqui)', não responda saudações, reponda apenas utilidades ou saberes populares ou dicas sobre os cultivos selecionados.\n"
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
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
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
        "user_id": user_id,
    })

