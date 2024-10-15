from django.db import models

class Seedbed(models.Model):
    nome = models.CharField(max_length=80, blank=False, null=False)
    community = models.ForeignKey('communities.Community', on_delete=models.CASCADE, related_name='seedbeds_in_community', null=True, blank=True)
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='seedbeds_in_product')  # Mudança para 'related_name'

    def __str__(self):
        return self.nome
