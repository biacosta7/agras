# Generated by Django 5.1.1 on 2024-10-15 01:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0002_community_seedbeds'),
        ('products', '0008_alter_product_seedbed'),
        ('seedbeds', '0002_remove_seedbed_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='seedbed',
            name='community',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seedbeds_in_community', to='communities.community'),
        ),
        migrations.AddField(
            model_name='seedbed',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seedbeds_in_product', to='products.product'),
        ),
    ]
