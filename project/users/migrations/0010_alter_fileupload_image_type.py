# Generated by Django 5.1.1 on 2024-11-29 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_fileupload_image_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='image_type',
            field=models.CharField(choices=[('profile', 'Profile'), ('banner', 'Banner'), ('community', 'Community'), ('seedbed', 'Seedbed')], default='banner', max_length=10),
        ),
    ]
