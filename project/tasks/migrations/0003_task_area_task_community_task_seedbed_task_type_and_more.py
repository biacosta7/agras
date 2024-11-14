# Generated by Django 5.1.1 on 2024-11-05 21:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('areas', '0002_initial'),
        ('communities', '0003_membershiprequest'),
        ('products', '0001_initial'),
        ('seedbeds', '0002_seedbed_area'),
        ('tasks', '0002_remove_task_time_task_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='area_tasks', to='areas.area'),
        ),
        migrations.AddField(
            model_name='task',
            name='community',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='community_tasks', to='communities.community'),
        ),
        migrations.AddField(
            model_name='task',
            name='seedbed',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seedbed_tasks', to='seedbeds.seedbed'),
        ),
        migrations.AddField(
            model_name='task',
            name='type',
            field=models.CharField(choices=[('community', 'Comunidade'), ('area', 'Área'), ('seedbed', 'Canteiro'), ('type_product', 'Tipo Produto'), ('product', 'Produto')], default='community', max_length=15),
        ),
        migrations.AddField(
            model_name='task',
            name='type_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='type_product_tasks', to='products.typeproduct'),
        ),
        migrations.AlterField(
            model_name='task',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_tasks', to='products.product'),
        ),
    ]