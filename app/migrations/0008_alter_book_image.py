# Generated by Django 5.1.3 on 2024-12-09 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_customuser_book_image_customuser_profile_image_chat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='book_img/'),
        ),
    ]
