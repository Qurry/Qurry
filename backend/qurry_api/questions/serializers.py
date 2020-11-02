from rest_framework import serializers

from .models import Question, Tag, Answer
from users.models import User


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'description']
    
    def create(self, validated_data):
        pass


class AnswerSerializer(serializers.HyperlinkedModelSerializer):

    body = serializers.CharField(max_length=500)
    user = serializers.SerializerMethodField('user_detail')

    question = serializers.SlugRelatedField(
        # many=True,
        # queryset=Question.objects.all(),
        read_only=True,
        slug_field='id'
    )
    votes = serializers.SerializerMethodField('calculate_votes')

    class Meta:
        model = Answer
        fields = ['id', 'body', 'votes', 'user', 'question']

    def calculate_votes(self, obj):
        return len(obj.vote_up_users.all()) - len(obj.vote_down_users.all())
    
    def user_detail(self, obj):
        return {'id': obj.user.id, 'username': obj.user.username}

class QuestionSerializer(serializers.HyperlinkedModelSerializer):

    title = serializers.CharField(max_length=200)
    body = serializers.CharField(max_length=500)

    tags = TagSerializer(
        many=True,
    )

    user = serializers.SerializerMethodField('user_detail')

    answers = serializers.SerializerMethodField('answers_number')
    votes = serializers.SerializerMethodField('calculate_votes')

    class Meta:
        model = Question
        fields = ['id', 'title', 'body', 'votes', 'tags', 'answers', 'votes', 'user']
    
    def create(self, validated_data):
        validated_data['user'] = User.objects.first()
        validated_data['votes'] = 0

        return super().create(validated_data)

    """def upgrade(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
       
        # instance.tags = validated_data.get('tags', instance.tags)

        instance.save()
        return instance """

    def answers_number(self, obj):
        return len(Answer.objects.filter(question=obj.id))

    def calculate_votes(self, obj):
        return len(obj.vote_up_users.all()) - len(obj.vote_down_users.all())

    def user_detail(self, obj):
        return {'id': obj.user.id, 'username': obj.user.username}

