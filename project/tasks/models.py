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
        ('unique', 'Única'),    
        ('daily', 'Diária'),
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
    
    community = models.ForeignKey(Community, related_name='community_tasks', on_delete=models.CASCADE, null=True, blank=True)
    area = models.ForeignKey(Area, related_name='area_tasks', on_delete=models.CASCADE, null=True, blank=True)
    seedbed = models.ForeignKey(Seedbed, related_name='seedbed_tasks', on_delete=models.CASCADE, null=True, blank=True)
    type_product = models.ForeignKey(TypeProduct, related_name='type_product_tasks', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, related_name='product_tasks', on_delete=models.CASCADE, null=True, blank=True)
    
    local = models.CharField(max_length=15, choices=TYPE_CHOICES, default='community')
    description = models.TextField(blank=False, null=False)
    is_completed = models.BooleanField(default=False)
    materials = models.TextField(blank=False, null=False)
    start_date = models.DateField(blank=False, null=True)
    final_date = models.DateField(null=False, blank=True)
    recurrence = models.CharField(max_length=10, choices=RECURRENCE_CHOICES, default='unique', null=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='to_do', null=False)
    responsible_users = models.ManyToManyField('users.User', blank=False)
    
    def __str__(self):
        return f"{self.description} ({self.get_type_display()}) - Local: {self.local} -  {'Finalizada' if self.is_completed else 'Pendente'}"
