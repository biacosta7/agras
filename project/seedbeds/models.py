from django.db import models
from areas.models import Area
class Seedbed(models.Model):
    nome = models.CharField(max_length=80, blank=False, null=False)
    area = models.ForeignKey(Area, related_name='seedbeds', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nome
