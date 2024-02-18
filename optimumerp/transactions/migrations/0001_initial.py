# Generated by Django 5.0.1 on 2024-02-13 01:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=255)),
                ('type', models.CharField(choices=[('IN', 'Entrada'), ('OUT', 'Saída')], max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.product')),
            ],
            options={
                'verbose_name': 'Transação',
                'verbose_name_plural': 'Transações',
            },
        ),
    ]
