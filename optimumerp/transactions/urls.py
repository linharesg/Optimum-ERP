from django.urls import path
from . import views

app_name = "transactions"

urlpatterns= [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("cadastro/", views.create, name="create"),
    path("estoque", views.inventory_index, name="inventory_index"),
    # path("inventory_search", views.inventory_search, name="inventory_search"),
]



