from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    endereco = models.CharField(max_length=255, blank=False, null=False)
    cidade = models.CharField(max_length=80, blank=False, null=False)
    estado = models.CharField(max_length=80, blank=False, null=False)
    cep = models.CharField(max_length=10, blank=False, null=False)
    data_nascimento = models.DateField(null=True, blank=True)
    # foto_perfil = models.ImageField(upload_to='perfil/', blank=True, null=True) VER COMO VAMOS ARMAZENAR IMAGENS NO DB (acredito que o SQLite não seja muito eficiente no 
                                                                                                                                                # armanzenamento de imagens)

    def __str__(self):
        return self.username
