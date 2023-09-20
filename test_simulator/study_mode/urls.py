from django.urls import path
from .views import study_mode, selected_test, selected_question, save_user_question_data


urlpatterns = [
    path('', study_mode, name='study_mode'),
    path('test/<int:test>/', selected_test, name='selected_test'),
    path('question/<int:question>/', selected_question, name='selected_question'),
    path('question/<int:question>/save/', save_user_question_data, name='save_user_question_data')
]   