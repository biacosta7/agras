# Generated by Django 5.1.1 on 2024-11-13 12:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_alter_task_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('low', 'Baixa'), ('medium', 'Média'), ('high', 'Alta')], default='low', max_length=15),
        ),
        migrations.AddField(
            model_name='task',
            name='responsible_users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]