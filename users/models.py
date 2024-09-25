from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    city = models.CharField(max_length=80, blank=False, null=False)
    state = models.CharField(max_length=80, blank=False, null=False)
    # profile_pic = models.ImageField(upload_to='perfil/', blank=True, null=True) VER COMO VAMOS ARMAZENAR IMAGENS NO DB (acredito que o SQLite não seja muito eficiente no 
                                                                                                                                                # armanzenamento de imagens)

    def __str__(self):
        return self.username
