# Generated by Django 5.1.1 on 2024-10-03 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seedbeds', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seedbed',
            name='product',
        ),
    ]
