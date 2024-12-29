# Generated by Django 5.1.3 on 2024-12-27 16:46

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_customuser_user_book_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
    ]