from django.urls import path
from . import views

app_name = "sales_order"

urlpatterns= [
    path("", views.SalesOrderListView.as_view(), name="index"),
    path("cadastro/get_sale_value/", views.get_sale_value, name="get_sale_value"),
    path("cadastro/", views.create, name="create"),
    path("editar/<int:id>/", views.update, name="update"),
    path("<int:id>/delete_product", views.delete_product_from_sale_order, name="delete_product"),
]