# Generated by Django 5.0.6 on 2024-06-03 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0005_artistavailability"),
    ]

    operations = [
        migrations.AddField(
            model_name="artistavailability",
            name="booked",
            field=models.BooleanField(default=False),
        ),
    ]