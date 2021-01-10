from django.urls import path

from .views import QuestionView, TagView, AnswerView, CommentView

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

    path('comments/',
         CommentView.as_view(), name='view-comments'),
    path('comments/<int:id>/',
         CommentView.as_view(), name='view-comment-details'),
    path('answers/<int:aid>/comments/',
         CommentView.as_view(), name='view-comments-of-answer'),
    path('questions/<int:qid>/comments/',
         CommentView.as_view(), name='view-answer-details'),

    path('tags/', TagView.as_view(), name='view-tags'),
]
