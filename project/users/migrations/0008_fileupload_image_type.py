# Generated by Django 5.1.1 on 2024-11-28 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_fileupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='image_type',
            field=models.CharField(choices=[('profile', 'Profile'), ('banner', 'Banner')], default='banner', max_length=10),
        ),
    ]