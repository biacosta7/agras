# Generated by Django 5.1.1 on 2024-11-13 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_task_area_task_community_task_seedbed_task_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateField(),
        ),
    ]