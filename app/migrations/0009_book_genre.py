# Generated by Django 5.1.3 on 2024-12-12 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_book_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.CharField(choices=[('fiction', 'Fiction'), ('mystery', 'Mystery'), ('fantasy', 'Fantasy'), ('sci-fi', 'Sci-Fi'), ('romance', 'Romance'), ('horror', 'Horror'), ('thriller', 'Thriller'), ('biography', 'Biography'), ('history', 'History'), ('self-help', 'Self-Help')], max_length=50, null=True),
        ),
    ]
