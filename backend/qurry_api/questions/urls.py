from django.urls import path, include

from .views import return_questions, view_question

urlpatterns = [
    path('', return_questions, name='show-questions'),
    path('/<int:qid>', view_question, name='view-question')
]
