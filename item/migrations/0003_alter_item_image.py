# Generated by Django 5.0.6 on 2024-07-18 19:29

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("item", "0002_carditems_user_item_card_item_is_available_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="image",
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name="img"),
        ),
    ]
