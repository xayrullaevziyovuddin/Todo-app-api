# Generated by Django 5.0.7 on 2024-11-16 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth_app", "0012_alter_customuser_email_delete_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="email_otp_code",
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="email_otp_expires",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]