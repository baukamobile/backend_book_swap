# Generated by Django 5.1.3 on 2024-12-14 13:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_book_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_books', to='app.customuser'),
        ),
    ]
