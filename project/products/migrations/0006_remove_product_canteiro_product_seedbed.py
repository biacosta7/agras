# Generated by Django 5.1.1 on 2024-10-04 00:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_canteiro'),
        ('seedbeds', '0002_remove_seedbed_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='canteiro',
        ),
        migrations.AddField(
            model_name='product',
            name='seedbed',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='seedbeds.seedbed'),
            preserve_default=False,
        ),
    ]