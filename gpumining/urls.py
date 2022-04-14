from django.urls import path
from gpumining import views

urlpatterns = [
    path('gpumining', views.gpumining, name='gpumining'),
    ]