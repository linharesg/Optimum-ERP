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
