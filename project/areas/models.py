from django.db import models

class Area(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    description = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    community = models.ForeignKey('communities.Community', related_name='areas', on_delete=models.CASCADE)  # Usando string para evitar importação circular

    def __str__(self):
        return self.name
