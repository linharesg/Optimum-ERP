from django.urls import path
from .views import PurchasesListView, PurchasesCreateView

app_name = "purchases"

urlpatterns = [
    path("", PurchasesListView.as_view(), name="index"),
    path("cadastrar/", PurchasesCreateView.as_view(), name="create"),
    # path("search", views.search, name="search"),
    # path("<int:id>/toggle_enabled", views.toggle_enabled, name="toggle_enabled"),
    # path("<int:id>/delete/", views.delete, name="delete"),
    # path("<slug:slug>/", views.ClientsUpdateView.as_view(), name="update"),
]
