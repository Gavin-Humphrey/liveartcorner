# Generated by Django 5.0.6 on 2024-06-19 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("item", "0006_alter_item_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item", name="image", field=models.ImageField(upload_to="img"),
        ),
    ]
