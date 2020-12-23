from django.urls import path, include
from django.http import JsonResponse

from .views import QuestionView, TagView, AnswerView


urlpatterns = [
    path('questions/', QuestionView.as_view(), name='view-questions'),
    path('questions/<int:id>/', QuestionView.as_view(),
         name='view-question-details'),

    path('questions/<int:qid>/answers/',
         AnswerView.as_view(), name='view-answers-of-question'),

    path('answers/',
         AnswerView.as_view(), name='view-answers'),
    path('answers/<int:id>/',
         AnswerView.as_view(), name='view-answer-details'),

    path('tags/', TagView.as_view(), name='view-tags'),
]
