# Generated by Django 5.0.6 on 2024-09-12 16:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0011_cartitem_cart_alter_cartitem_delivery_method"),
        ("order", "0002_deliveryinfo_city_deliveryinfo_country_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="delivery_method",
        ),
        migrations.RemoveField(
            model_name="orderitem",
            name="quantity",
        ),
        migrations.AddField(
            model_name="orderitem",
            name="delivery_method",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="cart.deliverymethod",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="orderitem",
            name="item_total_cost",
            field=models.DecimalField(decimal_places=2, default=250, max_digits=10),
            preserve_default=False,
        ),
    ]
