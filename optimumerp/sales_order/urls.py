from django.urls import path
from . import views

app_name = "sales_order"

urlpatterns= [
    path("", views.index, name="index"),
    path("novo/get_sale_value/", views.get_sale_value_create, name="get_sale_value_create"),
    path("novo/", views.create, name="create"),
    path("editar/<int:id>/get_sale_value/", views.get_sale_value_update, name="get_sale_value_update"),
    path("editar/<int:id>/", views.update, name="update"),
    path("<int:id>/delete_product", views.delete_product, name="delete_product"),
    path("<int:id>/products/", views.get_products_from_sale_order, name="products"),
    path("<int:id>/cancel/", views.cancel, name="cancel"),
    path("<int:id>/finish-order/", views.finish_order, name="finish_order")
]