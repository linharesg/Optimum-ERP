# Generated by Django 5.0.1 on 2024-02-24 16:21

import django.core.validators
import django.db.models.deletion
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Confirmado', 'Confirmado'), ('Pendente', 'Pendente'), ('Cancelado', 'Cancelado')], max_length=10)),
                ('delivery_date', models.DateField(blank=True, null=True)),
                ('total_value', models.DecimalField(decimal_places=2, max_digits=12)),
                ('discount', models.DecimalField(decimal_places=0, default=Decimal('0'), max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('installments', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(36)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clients.clients')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Pedido de venda',
                'verbose_name_plural': 'Pedidos de venda',
            },
        ),
        migrations.CreateModel(
            name='SalesOrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_value', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.01, message='Informe um valor válido')])),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.01, message='Informe um valor válido')])),
                ('total_value_product', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01, message='Informe um valor válido')])),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.product')),
                ('sale_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales_order.salesorder')),
            ],
            options={
                'verbose_name': 'Produto do pedido de venda',
                'verbose_name_plural': 'Produtos do pedido de venda',
                'unique_together': {('product', 'sale_order')},
            },
        ),
        migrations.AddField(
            model_name='salesorder',
            name='products',
            field=models.ManyToManyField(through='sales_order.SalesOrderProduct', to='products.product'),
        ),
    ]
