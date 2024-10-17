# Generated by Django 5.0.6 on 2024-09-02 10:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0006_alter_cartitem_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="cartitem",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="cartitem",
            name="quantity",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name="cartitem",
            name="cart",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="cart.cart"
            ),
        ),
        migrations.RemoveField(
            model_name="cartitem",
            name="delivery_method",
        ),
        migrations.RemoveField(
            model_name="cartitem",
            name="discount_code",
        ),
    ]