from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from media.models import DocumentAttach, ImageAttach
from mptt.models import MPTTModel, TreeForeignKey

from .managers import QuestionManager


class Post(models.Model):
    body = models.TextField('Body', default='', max_length=10000)

    created_at = models.DateTimeField('Creation Date', auto_now_add=True)
    updated_at = models.DateTimeField('Update Date', auto_now=True)

    user = models.ForeignKey(
        "users.User", verbose_name='Owner', on_delete=models.CASCADE)

    upvote_reward = 0
    downvote_penalty = 0

    class Meta:
        abstract = True

    def score_up(self, reverse=False):
        if reverse:
            self.user.add_to_score(-self.upvote_reward)
        else:
            self.user.add_to_score(self.upvote_reward)

    def score_down(self, reverse=False):
        if reverse:
            self.user.add_to_score(self.downvote_penalty)
        else:
            self.user.add_to_score(-self.downvote_penalty)

    def get_vote(self, user, action):
        # remove user from voters
        if self.vote_up_users.filter(id=user.id).exists():
            self.vote_up_users.remove(user)
            self.score_up(reverse=True)

        if self.vote_down_users.filter(id=user.id).exists():
            self.vote_down_users.remove(user)
            self.score_down(reverse=True)

        if action == '1':
            self.vote_up_users.add(user)
            self.score_up()
        elif action == '-1':
            self.vote_down_users.add(user)
            self.score_down()
        elif action == '0':
            pass
        else:
            raise ValueError('vote is invalid')

    def time_info(self):
        return {
            'createdAt': str(timezone.localtime(self.created_at).replace(microsecond=0)),
            'editedAt': str(timezone.localtime(self.updated_at).replace(microsecond=0)),
        }


class Comment(Post):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    reference_object = GenericForeignKey('content_type', 'object_id')

    upvote_reward = 5
    downvote_penalty = 0

    def __str__(self):
        return 'comment from %s' % self.user

    def as_preview(self):
        return {**self.time_info(), **{
            'id': str(self.id),
            'body': self.body,
            'user': self.user.as_preview()
        }}

    def as_detailed(self):
        return {**self.as_preview(), **{
            '%sId' % self.content_type.model: self.object_id,
        }}


class Tag(MPTTModel):
    name = models.CharField('Name', max_length=20)
    description = models.TextField('Description', blank=True, default='')

    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    @classmethod
    def get_all_roots(cls):
        return cls.objects.filter(level=0)

    @classmethod
    def all_as_preview(cls):
        return list(root.as_preview() for root in cls.get_all_roots())

    def as_preview(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'children': list(child_tag.as_preview() for child_tag in self.get_children())
        }

    def __str__(self):
        return self.name


class Question(Post):
    title = models.CharField('Title', max_length=200)
    tags = models.ManyToManyField(Tag, verbose_name='Tags', blank=True)

    comments = GenericRelation(Comment)

    images = GenericRelation(ImageAttach)
    documents = GenericRelation(DocumentAttach)

    vote_up_users = models.ManyToManyField(
        "users.User", verbose_name='Users who voted up this question', related_name='question_upvotes', blank=True)
    vote_down_users = models.ManyToManyField(
        "users.User", verbose_name='Users who voted down this question', related_name='question_downvotes', blank=True)

    objects = QuestionManager

    upvote_reward = 10
    downvote_penalty = 0

    def __str__(self):
        return '%d: %s' % (self.id, self.title)

    def vote_of(self, user):
        if user in self.vote_up_users.all():
            return 1
        if user in self.vote_down_users.all():
            return -1
        return 0

    def as_preview(self, user):
        return {**self.time_info(), **{
            'id': str(self.id),
            'title': self.title,
            'votes': self.vote_up_users.count() - self.vote_down_users.count(),
            'answers': self.answer_set.count(),
            'comments': self.comments.count(),
            'tagIds': list(str(tag.id) for tag in self.tags.all()),
            'user': self.user.as_preview(),
            'userVote': self.vote_of(user)
        }}

    def as_detailed(self, user):
        return {**self.as_preview(user), **{
            'body': self.body,
            'answers': list(answer.as_detailed(user) for answer in self.answer_set.all()),
            'comments': list(comment.as_preview() for comment in self.comments.all()),
            'images': list(image.file.as_preview() for image in self.images.all()),
            'documents': list(document.file.as_preview() for document in self.documents.all()),
        }}


class Answer(Post):
    question = models.ForeignKey(
        Question, verbose_name='Question', on_delete=models.CASCADE)

    comments = GenericRelation(Comment)

    images = GenericRelation(ImageAttach)
    documents = GenericRelation(DocumentAttach)

    upvote_reward = 10
    downvote_penalty = 0

    vote_up_users = models.ManyToManyField(
        "users.User", verbose_name='Users who voted up this answer', related_name='answer_upvotes', blank=True)
    vote_down_users = models.ManyToManyField(
        "users.User", verbose_name='Users who voted down this answer', related_name='answer_downvotes', blank=True)

    def __str__(self):
        return "Answer from %s" % self.user

    def count_votes(self):
        return self.vote_up_users.count() - self.vote_down_users.count()

    def vote_of(self, user):
        if user in self.vote_up_users.all():
            return 1
        if user in self.vote_down_users.all():
            return -1
        return 0

    def as_preview(self, user):
        return {**self.time_info(), **{
            'id': str(self.id),
            'body': self.body,
            'votes': self.count_votes(),
            'user': self.user.as_preview(),
            'userVote': self.vote_of(user)
        }}

    def as_detailed(self, user):
        return {**self.as_preview(user), **{
            'comments': list(comment.as_preview() for comment in self.comments.all()),
            'images': list(image.file.as_preview() for image in self.images.all()),
            'documents': list(document.as_preview() for document in self.documents.all()),
        }}
