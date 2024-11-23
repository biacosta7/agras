from django.db import models
from seedbeds.models import Seedbed
from communities.models import Community
from django.utils import timezone

class TypeProduct(models.Model):
    name = models.CharField(max_length=80, null=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='type_products', null=True)
    lifecycle = models.IntegerField(null=True, blank=True)
    total_colhido = models.IntegerField(default=0)
    actions_interval = models.JSONField(default=dict)  # Exemplo de dicionário: {"irrigação": 5, "poda": 10, "manejo": 7}
    taxa_colheita = models.FloatField(default=1.0)

    class Meta:
        unique_together = ('name', 'community')  # Garante que a combinação de nome e comunidade seja única

    def __str__(self):
        return self.name
    
    def atualizar_produtividade(self, quantidade_colhida):
        # Atualiza a quantidade total colhida
        self.total_colhido += quantidade_colhida
        self.save()
    
    def get_action_interval(self, action_name):
        """Retorna o intervalo da ação solicitada"""
        return self.actions_interval.get(action_name)

    def add_action_interval(self, action_name, interval):
        """Adiciona ou atualiza o intervalo de uma ação"""
        self.actions_interval[action_name] = interval
        self.save()

class Product(models.Model):
    type_product = models.ForeignKey(TypeProduct, on_delete=models.CASCADE, related_name='products', null=True)
    seedbed = models.ForeignKey(Seedbed, on_delete=models.CASCADE, related_name='products_in_seedbed', null=True, blank=True)  
    data_plantio = models.DateField(default=timezone.now)
    quantidade = models.IntegerField(default=1)
    quantidade_colhida = models.IntegerField(default=0, null=True, blank=True)
    data_colheita = models.DateField(null =True, blank = True)  # Campo para a data da colheita
    #is_harvested = models.BooleanField(default=False)  # Novo campo

    def get_absolute_url(self):
        return f"/products/{self.id}/"

    @property
    def name_type_product(self):
        return self.type_product.name
