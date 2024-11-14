from django.db import models
from seedbeds.models import Seedbed
from communities.models import Community
from django.utils import timezone

class TypeProduct(models.Model):
    name = models.CharField(max_length=80, null=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='type_products', null=True)
    lifecycle = models.IntegerField(null=True, blank=True)
    total_colhido = models.IntegerField(default=0)

    class Meta:
        unique_together = ('name', 'community')  # Garante que a combinação de nome e comunidade seja única

    def __str__(self):
        return self.name
    
    def atualizar_produtividade(self, quantidade_colhida):
        # Atualiza a quantidade total colhida
        self.total_colhido += quantidade_colhida
        self.save()

class Product(models.Model):
    type_product = models.ForeignKey(TypeProduct, on_delete=models.CASCADE, null=True)
    seedbed = models.ForeignKey(Seedbed, on_delete=models.CASCADE, related_name='products_in_seedbed', null=True, blank=True)  
    
    data_plantio = models.DateField()
    quantidade = models.IntegerField(default=1)

    def get_absolute_url(self):
        return f"/products/{self.id}/"

    @property
    def name_type_product(self):
        return self.type_product.name

class Harvest(models.Model):
    type_product = models.ForeignKey(TypeProduct, on_delete=models.CASCADE, related_name='harvests')
    seedbed = models.ForeignKey(Seedbed, on_delete=models.CASCADE, related_name='harvests', null=True, blank=True)
    quantidade_colhida = models.IntegerField(null = True, blank = True)  # Campo para a quantidade colhida
    data_colheita = models.DateTimeField(default=timezone.now)  # Campo para a data da colheita

    def __str__(self):
        return f"{self.quantidade_colhida} unidades de {self.type_product.name} colhidas em {self.data_colheita}"