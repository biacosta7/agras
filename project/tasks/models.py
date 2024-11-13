from django.db import models
from products.models import Product, TypeProduct
from seedbeds.models import Seedbed
from communities.models import Community
from areas.models import Area

class Task(models.Model):

    STATUS_CHOICES = [
        ('to_do', 'A Fazer'),
        ('in_progress', 'Em Progresso'),
        ('completed', 'Concluída'),
    ]
    
    RECURRENCE_CHOICES = [
        ('daily', 'Diário'),
        ('weekly', 'Semanal'),
        ('monthly', 'Mensal'),
        ('yearly', 'Anual'),
    ]

    TYPE_CHOICES = [
        ('community', 'Comunidade'),
        ('area', 'Área'),
        ('seedbed', 'Canteiro'),
        ('type_product', 'Tipo Produto'),
        ('product', 'Produto'),
    ]

    type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='community')
    
    community = models.ForeignKey(Community, related_name='community_tasks', on_delete=models.CASCADE, null=True, blank=True)
    area = models.ForeignKey(Area, related_name='area_tasks', on_delete=models.CASCADE, null=True, blank=True)
    seedbed = models.ForeignKey(Seedbed, related_name='seedbed_tasks', on_delete=models.CASCADE, null=True, blank=True)
    type_product = models.ForeignKey(TypeProduct, related_name='type_product_tasks', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, related_name='product_tasks', on_delete=models.CASCADE, null=True, blank=True)
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    deadline = models.DateField()
    recurrence = models.CharField(max_length=10, choices=RECURRENCE_CHOICES)
    status = models.CharField(max_length=100, null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     # Validações para garantir o preenchimento correto com base no tipo
    #     if self.type == 'product' and not self.product:
    #         raise ValueError("O campo 'product' deve ser preenchido quando o tipo é 'Produto'.")
    #     elif self.type == 'type_product' and not self.type_product:
    #         raise ValueError("O campo 'type_product' deve ser preenchido quando o tipo é 'Tipo Produto'.")
    #     elif self.type == 'seedbed' and not self.seedbed:
    #         raise ValueError("O campo 'seedbed' deve ser preenchido quando o tipo é 'Canteiro'.")
    #     elif self.type == 'community' and not self.community:
    #         raise ValueError("O campo 'community' deve ser preenchido quando o tipo é 'Comunidade'.")
    #     elif self.type == 'area' and not self.area:
    #         raise ValueError("O campo 'area' deve ser preenchido quando o tipo é 'Área'.")

    #     # Define campos não correspondentes como None
    #     if self.type != 'product':
    #         self.product = None
    #     if self.type != 'type_product':
    #         self.type_product = None
    #     if self.type != 'seedbed':
    #         self.seedbed = None
    #     if self.type != 'community':
    #         self.community = None
    #     if self.type != 'area':
    #         self.area = None

        #super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} ({self.get_type_display()}) - {'Finalizada' if self.is_completed else 'Pendente'}"
