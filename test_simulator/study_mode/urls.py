from django.urls import path
from .views import study_mode, selected_test, selected_question


urlpatterns = [
    path('', study_mode, name='study_mode'),
    path('test/<int:test>/', selected_test, name='selected_test'),
    path('test/<int:test>/question/<int:question>/', selected_question, name='selected_question'),
]   