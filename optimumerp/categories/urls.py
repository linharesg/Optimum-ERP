from django.urls import path
from . import views
from .views import CategoryListView

app_name = "categories"
urlpatterns = [
    path("", CategoryListView.as_view(), name="index"),
    path("cadastro/", views.create, name="create"),
    path("update/<int:id>/", views.update, name="update"),
    path("delete/<int:id>/delete/", views.delete, name="delete"),
]