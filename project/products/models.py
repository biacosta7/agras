from django.db import models
from seedbeds.models import Seedbed
from communities.models import Community

class TypeProduct(models.Model):
    name = models.CharField(max_length=80, null=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='type_products', null=True)
    lifecycle = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('name', 'community')  # Garante que a combinação de nome e comunidade seja única

    def __str__(self):
        return self.name

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