# Generated by Django 5.0.2 on 2024-02-27 22:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('sales_order', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='salesorder',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='salesorderproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.product'),
        ),
        migrations.AddField(
            model_name='salesorderproduct',
            name='sale_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales_order.salesorder'),
        ),
        migrations.AddField(
            model_name='salesorder',
            name='products',
            field=models.ManyToManyField(through='sales_order.SalesOrderProduct', to='products.product'),
        ),
        migrations.AlterUniqueTogether(
            name='salesorderproduct',
            unique_together={('product', 'sale_order')},
        ),
    ]
