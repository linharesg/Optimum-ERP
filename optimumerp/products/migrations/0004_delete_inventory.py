# Generated by Django 5.0.1 on 2024-02-13 23:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_delete_productinventory'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Inventory',
        ),
    ]
