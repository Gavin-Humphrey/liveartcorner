# Generated by Django 4.2.11 on 2024-09-24 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("item", "0012_alter_item_image"),
        ("order", "0005_remove_orderitem_discount_code_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="quantity",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterUniqueTogether(
            name="orderitem",
            unique_together={("order", "item")},
        ),
    ]
