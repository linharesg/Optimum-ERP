from django.urls import path
from . import views

app_name = "products"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("cadastro", views.create, name="create"),
    path("<slug:slug>", views.update, name="update"),
    path("<int:id>/toggle_enabled", views.toggle_enabled, name="toggle_enabled"),
    path("<int:id>/delete", views.delete, name="delete"),
    path("<int:id>/suppliers/", views.get_suppliers_from_product, name="suppliers"),
    path("<int:id>/delete_supplier", views.delete_supplier_from_product, name="delete_supplier")
]
