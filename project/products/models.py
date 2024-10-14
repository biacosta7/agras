from django.db import models
from seedbeds.models import Seedbed

class TypeProduct(models.Model):
    nome = models.CharField(max_length=80, null=True, unique=True)

    def __str__(self):
        return self.nome

class Product(models.Model):
    nome = models.ForeignKey(TypeProduct, on_delete=models.CASCADE, to_field='nome', null=True)
    data_plantio = models.DateField(auto_now_add=True)
    quantidade = models.IntegerField(default=1)
    seedbed = models.ForeignKey(Seedbed, on_delete=models.CASCADE)  # Chave estrangeira para Seedbed


    def get_absolute_url(self):
        return f"/products/{self.id}/"

    @property
    def nome_type_product(self):
        return self.nome.nome