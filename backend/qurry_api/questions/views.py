from rest_framework import viewsets
from rest_framework import permissions
from django.http import JsonResponse

from .models import Question, Answer, Tag
from users.models import User
from .serializers import QuestionSerializer, TagSerializer, AnswerSerializer


class QuestionViewSet(viewsets.ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    # permission_classes = [permissions.IsAuthenticated]

class TagViewSet(viewsets.ModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # permission_classes = [permissions.IsAuthenticated]

class AnswerViewSet(viewsets.ModelViewSet):

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]
