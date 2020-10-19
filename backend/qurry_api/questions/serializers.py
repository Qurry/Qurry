from rest_framework import serializers

from .models import Question, Tag, Answer


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['url', 'id', 'name', 'description']


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='id'
    )

    question = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='id'
    )

    class Meta:
        model = Answer
        fields = ['url', 'id', 'body', 'votes', 'user', 'question']


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    answers = serializers.SerializerMethodField('answers_number')

    class Meta:
        model = Question
        fields = ['url', 'id', 'title', 'votes', 'tags', 'answers']

    def answers_number(self, obj):
        return len(Answer.objects.filter(question=obj.id))

