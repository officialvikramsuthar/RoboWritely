# Generated by Django 4.2.4 on 2024-01-12 10:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("PriceCompare", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="discprice",
            name="price_per_tb",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="discprice",
            name="capacity",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="discprice",
            name="condition",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="discprice",
            name="form_factor",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="discprice",
            name="name",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="discprice",
            name="technology",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="discprice",
            name="warranty",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
