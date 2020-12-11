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
    dateTime = serializers.SerializerMethodField('data_time')

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )

    user = serializers.SerializerMethodField('user_detail')

    answers = serializers.SerializerMethodField('answers_number')
    votes = serializers.SerializerMethodField('calculate_votes')

    class Meta:
        model = Question
        fields = ['id', 'title', 'body', 'votes', 'dateTime', 'tags', 'answers', 'votes', 'user']
    
    def is_valid(self, raise_exception=False):
        self.initial_data['tags'] = self.initial_data['tagIds']
        super().is_valid(raise_exception)

    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['votes'] = 0

        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super(QuestionSerializer, self).to_representation(instance)
        representation['tags'] = TagSerializer(instance.tags.all(), many=True).data
        return representation

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
    
    def data_time(self, obj):
        return obj.date_time

