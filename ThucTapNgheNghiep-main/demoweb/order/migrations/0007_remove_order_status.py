# Generated by Django 4.2.3 on 2023-07-16 16:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0006_rename_users_cart_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="status",
        ),
    ]
