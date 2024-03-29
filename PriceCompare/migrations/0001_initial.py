# Generated by Django 4.2.4 on 2024-01-02 05:56

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DiscPrice",
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
                ("country", models.CharField(blank=True, default="USA", max_length=10)),
                ("price", models.FloatField(blank=True, default=10, null=True)),
                ("capacity", models.CharField(blank=True, max_length=50, null=True)),
                ("warranty", models.CharField(blank=True, max_length=50, null=True)),
                ("form_factor", models.CharField(blank=True, max_length=50, null=True)),
                ("technology", models.CharField(blank=True, max_length=50, null=True)),
                ("condition", models.CharField(blank=True, max_length=50, null=True)),
                ("name", models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
