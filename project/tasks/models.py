from django.db import models
from products.models import Product

class Task(models.Model):
    
    TIME_CHOICES = [
        ("morning", 'Manhã'),
        ("afternoon", 'Tarde'),
        ("full_day", 'Dia todo'),
    ]

    RECURRENCE_CHOICES = [
        ('daily', 'Diário'),
        ('weekly', 'Semanal'),
        ('monthly', 'Mensal'),
        ('yearly', 'Anual'),
    ]

    product = models.ForeignKey(Product, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    deadline = models.DateTimeField()
    recurrence = models.CharField(max_length=10, choices=RECURRENCE_CHOICES)
    time = models.CharField(max_length=10, choices=TIME_CHOICES)

    def __str__(self):
        return f"{self.title} ({'Finalizada' if self.is_completed else 'Pendente'})"
