from django.urls import path
from . import views

app_name = "sales_order"

urlpatterns= [
    path("", views.SalesOrderListView.as_view(), name="index"),
    # path("cadastro/", views.SalesOrderCreateView.as_view(), name="create"),
    path("cadastro/", views.create, name="create"),
    # path("", views.index, name="index"),
    # path("search", views.search, name="search"),
    # path("<int:id>/toggle_enabled", views.toggle_enabled, name="toggle_enabled"),
    # path("<int:id>/delete/", views.delete, name="delete"),
    # path("cadastro/", views.create, name="create"),
    # path("<slug:slug>/", views.ClientsUpdateView.as_view(), name="update"),
]