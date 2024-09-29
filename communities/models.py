from django.db import models
from users.models import User
# from seedbeds.models import Seedbed importar o model de Canteiros

class Community(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)  
    creator = models.ForeignKey(User,on_delete=models.CASCADE, related_name='created_communities')
    members = models.ManyToManyField(User, related_name='communities_members')
    # seedbeds = models.ForeignKey(Seedbed, on_delete=models.CASCADE, null=True, blank=True) FK para Canteiros
    # community_pic = models.ImageField(upload_to='community_pics/', blank=True, null=True)

    def __str__(self):
        return self.name