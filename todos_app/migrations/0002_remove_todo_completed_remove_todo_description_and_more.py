# Generated by Django 5.0.7 on 2024-10-26 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todos_app", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="todo",
            name="completed",
        ),
        migrations.RemoveField(
            model_name="todo",
            name="description",
        ),
        migrations.AddField(
            model_name="todo",
            name="status",
            field=models.CharField(
                choices=[("pending", "Pending"), ("completed", "Completed")],
                default=0,
                max_length=10,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="todo",
            name="title",
            field=models.CharField(max_length=255),
        ),
    ]
