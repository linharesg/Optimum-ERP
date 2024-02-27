from django.urls import path
from .views import DashView

app_name = 'dashboard'  # Definindo o namespace

urlpatterns = [
    path('', DashView.as_view(), name='index'),
]