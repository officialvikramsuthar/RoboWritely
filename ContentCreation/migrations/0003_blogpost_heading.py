# Generated by Django 4.2.4 on 2023-09-23 15:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ContentCreation", "0002_blogpost_paragraph_delete_content_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogpost",
            name="heading",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
