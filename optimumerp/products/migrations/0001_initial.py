# Generated by Django 5.0.1 on 2024-02-27 21:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        ('suppliers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('description', models.TextField()),
                ('sale_price', models.DecimalField(decimal_places=2, max_digits=255)),
                ('cst', models.CharField(choices=[('', 'Escolha o CST'), ('200', '200'), ('210', '210'), ('220', '220'), ('230', '230'), ('240', '240'), ('241', '241'), ('250', '250'), ('251', '251'), ('260', '260'), ('270', '270'), ('290', '290'), ('300', '300'), ('310', '310'), ('320', '320'), ('330', '330'), ('340', '340'), ('341', '341'), ('350', '350'), ('351', '351'), ('360', '360'), ('370', '370'), ('390', '390'), ('400', '400'), ('410', '410'), ('420', '420'), ('430', '430'), ('440', '440'), ('441', '441'), ('450', '450'), ('451', '451'), ('460', '460'), ('470', '470'), ('490', '490'), ('500', '500'), ('510', '510'), ('520', '520'), ('530', '530'), ('540', '540'), ('541', '541'), ('550', '550'), ('551', '551'), ('560', '560'), ('570', '570'), ('590', '590'), ('600', '600'), ('610', '610'), ('620', '620'), ('630', '630'), ('640', '640'), ('641', '641'), ('650', '650'), ('651', '651'), ('660', '660'), ('670', '670'), ('690', '690'), ('700', '700'), ('710', '710'), ('720', '720'), ('730', '730'), ('740', '740'), ('741', '741'), ('750', '750'), ('751', '751'), ('760', '760'), ('770', '770'), ('790', '790'), ('800', '800'), ('810', '810'), ('820', '820'), ('830', '830'), ('840', '840'), ('841', '841'), ('850', '850'), ('851', '851'), ('860', '860'), ('870', '870'), ('890', '890'), ('900', '900'), ('910', '910'), ('920', '920'), ('930', '930'), ('940', '940'), ('941', '941'), ('950', '950'), ('951', '951'), ('960', '960'), ('970', '970'), ('990', '990')], max_length=255)),
                ('minimum_stock', models.DecimalField(decimal_places=2, default=1, max_digits=255)),
                ('unit_of_measurement', models.CharField(choices=[('', 'Escolha a unidade de medida'), ('KG', 'Quilograma'), ('Metro', 'Metro'), ('Litro', 'Litro'), ('Unidade', 'Unidade')], max_length=7)),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('enabled', models.BooleanField(default=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='categories.category')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
            },
        ),
        migrations.CreateModel(
            name='SupplierProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suppliers.suppliers')),
            ],
            options={
                'verbose_name': 'Fornecedor do Produto',
                'verbose_name_plural': 'Fornecedores do Produto',
                'unique_together': {('supplier', 'product')},
            },
        ),
        migrations.AddField(
            model_name='product',
            name='suppliers',
            field=models.ManyToManyField(blank=True, through='products.SupplierProduct', to='suppliers.suppliers'),
        ),
    ]
