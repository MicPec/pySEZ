# Generated by Django 4.1.3 on 2022-12-05 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Status",
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
                ("name", models.CharField(max_length=50)),
                ("color", models.CharField(default="#eeeeee", max_length=7)),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("NOT_SET", ""),
                            ("NEW", "New"),
                            ("PROGRESS", "In progress"),
                            ("DONE", "Done"),
                        ],
                        default="NOT_SET",
                        max_length=8,
                    ),
                ),
            ],
        ),
    ]
