from django.urls import path
from . import views

app_name = "purchases"

urlpatterns = [
    path("", views.index, name="index"),
    path("novo/get_purchasing_price/", views.get_purchasing_price_create, name="get_purchasing_price_create"),
    path("editar/<int:id>/get_purchasing_price/", views.get_purchasing_price_update, name="get_purchasing_price_update"),
    path("novo/", views.create, name="create"),
    path("editar/<int:id>/", views.update, name="update"),
    path("<int:id>/delete_product", views.delete_product_from_purchase, name="delete_product"),
    path("<int:id>/products/", views.get_products_from_purchase, name="products"),
    path("<int:id>/cancel/", views.cancel, name="cancel"),
    path("<int:id>/finish-order/", views.finish_order, name="finish_order")
]