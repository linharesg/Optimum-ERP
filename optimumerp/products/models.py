from django.db import models
from django.utils.text import slugify

# Create your models here.
class Product(models.Model):
    MEASUREMENT_CHOICES = {
        "KG": "Quilograma",
        "Metro": "Metro",
        "Litro": "Litro",
        "Unidade": "Unidade"
    }
    CST_CHOICES = {
        "200": "200",
        "210": "210",
        "220": "220",
        "230": "230",
        "240": "240",
        "241": "241",
        "250": "250",
        "251": "251",
        "260": "260",
        "270": "270",
        "290": "290",
        "300": "300",
        "310": "310",
        "320": "320",
        "330": "330",
        "340": "340",
        "341": "341",
        "350": "350",
        "351": "351",
        "360": "360",
        "370": "370",
        "390": "390",
        "400": "400",
        "410": "410",
        "420": "420",
        "430": "430",
        "440": "440",
        "441": "441",
        "450": "450",
        "451": "451",
        "460": "460",
        "470": "470",
        "490": "490",
        "500": "500",
        "510": "510",
        "520": "520",
        "530": "530",
        "540": "540",
        "541": "541",
        "550": "550",
        "551": "551",
        "560": "560",
        "570": "570",
        "590": "590",
        "600": "600",
        "610": "610",
        "620": "620",
        "630": "630",
        "640": "640",
        "641": "641",
        "650": "650",
        "651": "651",
        "660": "660",
        "670": "670",
        "690": "690",
        "700": "700",
        "710": "710",
        "720": "720",
        "730": "730",
        "740": "740",
        "741": "741",
        "750": "750",
        "751": "751",
        "760": "760",
        "770": "770",
        "790": "790",
        "800": "800",
        "810": "810",
        "820": "820",
        "830": "830",
        "840": "840",
        "841": "841",
        "850": "850",
        "851": "851",
        "860": "860",
        "870": "870",
        "890": "890",
        "900": "900",
        "910": "910",
        "920": "920",
        "930": "930",
        "940": "940",
        "941": "941",
        "950": "950",
        "951": "951",
        "960": "960",
        "970": "970",
        "990": "990"
    }
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    sale_price = models.FloatField()
    is_perishable = models.BooleanField()
    expiration_date = models.DateField(null=True, blank=True)
    unit_of_measurement = models.CharField(max_length=7, choices=MEASUREMENT_CHOICES)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
