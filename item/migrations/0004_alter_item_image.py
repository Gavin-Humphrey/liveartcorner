# Generated by Django 5.0.6 on 2024-07-18 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("item", "0003_alter_item_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="image",
            field=models.ImageField(upload_to="img"),
        ),
    ]
