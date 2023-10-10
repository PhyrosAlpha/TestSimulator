from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('auth/login', views.auth_login, name='auth_login'),
    path('auth/logout', views.auth_logout, name='auth_logout'),
    path('simulator/', views.simulator, name='simulator'),
    path('simulator/test/<int:test>', views.start_simulator, name='simulator'),
    path('simulator/test/start/<int:test>', views.get_test, name='simulator_start'),
]   