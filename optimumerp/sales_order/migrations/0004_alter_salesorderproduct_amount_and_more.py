# Generated by Django 5.0.2 on 2024-02-14 11:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_order', '0003_rename_total_value_salesorderproduct_total_value_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesorderproduct',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.01, message='Informe um valor válido')]),
        ),
        migrations.AlterField(
            model_name='salesorderproduct',
            name='total_value_product',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01, message='Informe um valor válido')]),
        ),
        migrations.AlterField(
            model_name='salesorderproduct',
            name='unit_value',
            field=models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.01, message='Informe um valor válido')]),
        ),
    ]
