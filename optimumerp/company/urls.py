from django.urls import path
from . import views

app_name = "company"

urlpatterns= [
    path("dados/", views.index, name="index"),
    path("update-company/<int:id>/", views.update, name="update")
]