from django.db import models
from django.conf import settings

class ChatBot(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text_input = models.TextField()  
    gemini_output = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)  
    
    def __str__(self):
        return f"{self.user.username}: {self.text_input[:50]}"  # Exibindo apenas os primeiros 50 caracteres
