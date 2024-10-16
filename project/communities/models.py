from django.db import models
from users.models import User
from seedbeds.models import Seedbed

class Community(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    description = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User,on_delete=models.CASCADE, related_name='created_communities')
    members = models.ManyToManyField(User, related_name='communities_members')
    admins = models.ManyToManyField(User, related_name='admin_communities', blank=True)
    seedbeds = models.ManyToManyField(Seedbed, related_name='communities') #FK para Canteiros
    # community_pic = models.ImageField(upload_to='community_pics/', blank=True, null=True)

    def __str__(self):
        return self.name