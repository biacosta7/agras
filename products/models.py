from django.db import models
#from seedbeds.models import Seedbed #Ver o nome da classe Seedbed

class TypeProduct():
    nome = "tomate"

class Product(models.Model):
    nome = models.ForeignKey(TypeProduct, on_delete=models.CASCADE) #vira FK (id) de TypeProduct
    
    data_plantio = models.DateField()

    #necessidade_manejo = models.BooleanField()
    
    #produtividade_esperada = #formula desconhecida

    quantidade = models.IntegerField()

    #previsao_colheita = #formula desconhecida

    def get_absolute_url(self):
        return f"/products/{self.id}/"  