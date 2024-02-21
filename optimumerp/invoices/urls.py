from django.urls import path
from . import views

app_name = "invoices"

urlpatterns= [
    path("<int:id>/", views.open_invoice, name="open_invoice"),
    path("create-invoice/<int:id>/", views.create_invoice, name="create_invoice")
]