# Generated by Django 5.0.1 on 2024-02-14 00:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_inventory_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Inventory',
        ),
    ]
