from django.urls import path
from . import views

app_name = "transactions"

urlpatterns= [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("cadastro/", views.create, name="create")
]



