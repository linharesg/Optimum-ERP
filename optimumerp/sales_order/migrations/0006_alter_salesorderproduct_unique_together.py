# Generated by Django 5.0.1 on 2024-02-17 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('sales_order', '0005_alter_salesorderproduct_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='salesorderproduct',
            unique_together={('product', 'sale_order')},
        ),
    ]