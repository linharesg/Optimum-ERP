# Generated by Django 5.0.1 on 2024-02-10 20:40
=======
# Generated by Django 5.0.1 on 2024-02-09 15:40


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_product_maximum_stock_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='minimum_stock',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=255),
        ),
    ]
