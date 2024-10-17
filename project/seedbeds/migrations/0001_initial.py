# Generated by Django 5.1.1 on 2024-10-03 19:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0004_typeproduct_alter_product_data_plantio_product_nome'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seedbed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=80)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seedbeds', to='products.product')),
            ],
        ),
    ]
