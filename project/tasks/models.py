from django.db import models
from products.models import Product, TypeProduct
from seedbeds.models import Seedbed
from communities.models import Community
from areas.models import Area

class Task(models.Model):

    STATUS_CHOICES = [
        ('to_do', 'Pendente'),
        ('in_progress', 'Progresso'),
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
        ('product', 'Cultivo'),
        ('type_product', 'Tipo Cultivo'),
    ]

    PRIORITY = [
        ('low', 'Baixa'),
        ('medium', 'Média'),
        ('high', 'Alta'),
    ]

    
    community = models.ForeignKey(Community, related_name='community_tasks', on_delete=models.CASCADE, null=True, blank=True)
    area = models.ForeignKey(Area, related_name='area_tasks', on_delete=models.CASCADE, null=True, blank=True)
    seedbed = models.ForeignKey(Seedbed, related_name='seedbed_tasks', on_delete=models.CASCADE, null=True, blank=True)
    type_product = models.ForeignKey(TypeProduct, related_name='type_product_tasks', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, related_name='product_tasks', on_delete=models.CASCADE, null=True, blank=True)
    
    local = models.CharField(max_length=15, choices=TYPE_CHOICES, default='community')
    title = models.CharField(max_length=255, blank=False, null=True)
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    start_date = models.DateField(blank=False, null=False)
    final_date = models.DateField(blank=False, null=False)
    # recurrence = models.CharField(max_length=10, choices=RECURRENCE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='to-do', null=True)
    responsible_users = models.ManyToManyField('users.User', blank=True)
    priority = models.CharField(max_length=15, choices=PRIORITY, default='low')
    
    def __str__(self):
        return f"{self.title} ({self.get_type_display()}) - {'Finalizada' if self.is_completed else 'Pendente'}"
