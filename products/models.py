from django.db import models
from django.urls import reverse

# Create your models here.
# nome /
# especie /
# canteiro (default=None)
# data_plantio /
# observacoes /
# produtividade_esperada 
# quantidade /
# necessidade_manejo /
# previsao_colheita

class Product(models.Model):
    nome = models.CharField(max_length=100, blank=False)
    
    especie = models.CharField(max_length=100, blank=False)
    
    #seedbeds = models.
    #falta implementar seedbeds

    data_plantio = models.DateTimeField(auto_now_add=True)

    observacoes = models.TextField(null=True)

    necessidade_manejo = models.BooleanField() # null=True or defalut=True (checkbox)

    # blank=False (means that the field is required) null=False (means that it can be empty in the database) 
    
    #produtividade_esperada = 
    #formula desconhecida e :p

    quantidade = models.IntegerField(default = 1)

    #previsao_colheita = 
    #formula desconhecida 2 e :p

    def get_absolute_url(self):
        return f"/products/{self.id}/"