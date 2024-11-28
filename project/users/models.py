from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=80, blank=False, null=True)
    state = models.CharField(max_length=80, blank=False, null=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    # profile_pic = models.ImageField(upload_to='perfil/', blank=True, null=True) VER COMO VAMOS ARMAZENAR IMAGENS NO DB (acredito que o SQLite não seja muito eficiente no armanzenamento de imagens)

    def __str__(self):
        return self.username

class FileUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='uploads/')  # Diretório onde a imagem será salva
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Data de upload
    image_type = models.CharField(max_length=10, choices=[('profile', 'Profile'), ('banner', 'Banner')], default='banner')

    def __str__(self):
        return f"{self.user.username} - {self.image_type}"


