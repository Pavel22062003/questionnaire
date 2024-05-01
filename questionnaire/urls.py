from django.urls import path
from . import views
from questionnaire.apps import QuestionnaireConfig

app_name = QuestionnaireConfig.name

urlpatterns = [
    path('', views.list_questions, name='list_questions'),
    path('start/<str:questionnaire_id>/', views.start_questions, name='start_questions'),
    path('pass_survey/<str:block_id>', views.survey_question, name='survey_question'),
    path('final_page/<str:block_id>/', views.final_page, name='final_page'),
]
