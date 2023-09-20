from django.urls import path, include
from .views import TestList

urlpatterns = [
    path('', TestList.as_view(), name='get_test_list'),

]