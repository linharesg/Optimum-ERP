from django.urls import path
from . import views

app_name = "clients"

urlpatterns= [
    path("", views.index, name="index"),
    path("<int:id>/toggle_enabled", views.toggle_enabled, name="toggle_enabled"),
    path("<int:id>/delete/", views.delete, name="delete"),
    path("cadastro/", views.create, name="create"),
    path("<slug:slug>/", views.ClientsUpdateView.as_view(), name="update"),
]