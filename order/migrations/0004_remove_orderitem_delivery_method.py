# Generated by Django 5.0.6 on 2024-09-13 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0003_remove_order_delivery_method_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderitem",
            name="delivery_method",
        ),
    ]