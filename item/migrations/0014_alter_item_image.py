# Generated by Django 5.0.6 on 2024-06-29 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("item", "0013_alter_item_popularity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="image",
            field=models.ImageField(upload_to="img"),
        ),
    ]
