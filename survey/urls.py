from django.urls import path
from survey.views import SurveyDetailView, SurveyCreateView

urlpatterns = [
    path('survey/<int:user_id>/', SurveyDetailView.as_view(), name='survey_detail'),
    path('surveys/', SurveyCreateView.as_view(), name='survey-create'),
]
