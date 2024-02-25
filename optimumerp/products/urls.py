from django.urls import path
from . import views
from .views import CategoryListView

app_name = "products"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("cadastro", views.create, name="create"),
    path("<slug:slug>", views.update, name="update"),
    path("<int:id>/toggle_enabled", views.toggle_enabled, name="toggle_enabled"),
    path("<int:id>/delete", views.delete, name="delete"),
    path("<int:id>/suppliers/", views.get_suppliers_from_product, name="suppliers"),
    path("<int:id>/delete_supplier", views.delete_supplier_from_product, name="delete_supplier"),
    path("categorias/", CategoryListView.as_view(), name="categories"),
    path("categories/search", views.search_categories, name="categories_search"),
    path("categorias/cadastro/", views.create_category, name="category_create"),
    path("categorias/<int:id>/", views.update_category, name="category_update"),
    path("categories/<int:id>/delete/", views.delete_category, name="category_delete"),
]