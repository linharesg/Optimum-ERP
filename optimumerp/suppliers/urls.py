from django.urls import path
from . import views

app_name = "suppliers"

urlpatterns= [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("<int:id>/toggle_enabled", views.toggle_enabled, name="toggle_enabled"),
    path("<int:id>/delete/", views.delete, name="delete"),
    path("cadastro/", views.create, name="create"),
]