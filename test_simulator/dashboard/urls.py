from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('change_password/', views.change_password, name='change_password'),
    path('auth/change_password/', views.auth_change_password, name='auth_change_password'),
]