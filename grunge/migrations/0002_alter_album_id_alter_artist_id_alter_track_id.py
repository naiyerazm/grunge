# Generated by Django 5.1.3 on 2024-11-06 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("grunge", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="album",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="artist",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="track",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
