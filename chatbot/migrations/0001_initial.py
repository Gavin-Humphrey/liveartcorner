# Generated by Django 5.0.6 on 2024-07-25 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Statement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.CharField(max_length=1024)),
                ("search_text", models.CharField(max_length=1024)),
                ("conversation", models.CharField(max_length=1024)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "in_response_to",
                    models.CharField(blank=True, max_length=1024, null=True),
                ),
                ("search_in_response_to", models.CharField(max_length=1024)),
                ("persona", models.CharField(blank=True, max_length=1024, null=True)),
            ],
            options={
                "db_table": "statement",
            },
        ),
    ]
