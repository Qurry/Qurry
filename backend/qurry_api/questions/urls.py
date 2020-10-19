from django.urls import path, include
from rest_framework import routers

from .views import QuestionViewSet, TagViewSet, AnswerViewSet

router = routers.DefaultRouter()

router.register(r'questions', QuestionViewSet)
router.register(r'tags', TagViewSet)
router.register(r'answers', AnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
