from django.db import models

# Modelo Seedbed
class Seedbed(models.Model):  # Certifique-se de herdar de models.Model
    nome = models.CharField(max_length=80, blank=False, null=False)
    # profile_pic = models.ImageField(upload_to='perfil/', blank=True, null=True) VER COMO VAMOS ARMAZENAR IMAGENS NO DB (acredito que o SQLite não seja muito eficiente no 
    
    def __str__(self):
        return self.nome

