# Generated by Django 5.0.6 on 2024-07-19 16:41

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("item", "0006_alter_item_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="image",
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name="img"),
        ),
    ]
