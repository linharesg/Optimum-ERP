from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    """
    Um modelo para representar uma categoria.

    Atributos:
        name (models.CharField): Um campo para o nome da categoria.
        description (models.TextField): Um campo para a descrição da categoria.
        slug (models.SlugField): Um campo para armazenar o slug da categoria.

    Métodos:
        __str__: Retorna uma representação de string do objeto Category.
        save: Sobrescreve o método save para gerar e salvar o slug da categoria.
    """
    name = models.CharField(max_length=255, unique=True, verbose_name="Nome")
    description = models.TextField(verbose_name="Descrição")
    slug = models.SlugField(max_length=255, unique=True, editable=False)

    def __str__(self):
        """
        Retorna uma representação de string do objeto Category.

        Retorna:
            str: O nome da categoria.
        """
        return self.name
    
    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para gerar e salvar o slug da categoria.
        """
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        """
        Classe interna que fornece metadados associados ao modelo.

        Atributos:
            verbose_name (str): Um nome legível para humanos para o modelo no singular.
            verbose_name_plural (str): Um nome legível para humanos para o modelo no plural.
        """
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"