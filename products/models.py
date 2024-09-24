from django.db import models
#from seedbeds.models import Seedbed #Ver o nome da classe Seedbed

class Product(models.Model):
    nome = models.CharField(max_length=100, blank=False)
    
    especie = models.CharField(max_length=100, blank=False)
    
    #seedbeds = models.ForeignKey(Seedbed, on_delete=models.SET_NULL, null=True, related_name='seedbeds_products')

    #data_plantio = models.ForeignKey(Seedbed, on_delete=models.SET_NULL, null=True, related_name='data_plantio_products')

    #observacoes = models.ForeignKey(Seedbed, on_delete=models.SET_NULL, null=True, related_name='observacoes_products')

    #necessidade_manejo = models.BooleanField()
    
    #produtividade_esperada = #formula desconhecida

    #quantidade = models.ForeignKey(Seedbed, on_delete=models.SET_NULL, null=True, related_name='quantidade_products')

    #previsao_colheita = #formula desconhecida

    def get_absolute_url(self):
        return f"/products/{self.id}/"