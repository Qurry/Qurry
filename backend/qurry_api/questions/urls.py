from django.urls import path, include
from django.http import JsonResponse

from .views import QuestionView, TagView


urlpatterns = [
    path('questions/', QuestionView.as_view(), name='view-questions'),
    path('questions/<int:id>/', QuestionView.as_view(),
         name='view-question-details'),

    path('tags/', TagView.as_view(), name='view-tags'),
]
