from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from media.models import DocumentAttach, ImageAttach
from mptt.models import MPTTModel, TreeForeignKey

from .managers import QuestionManager


class VotedPostMixin(models.Model):
    votes = models.IntegerField('Votes', default=0)

    upvote_reward = 0
    downvote_penalty = 0

    vote_up_users = models.ManyToManyField(
        "users.User", verbose_name='Upvoting Users', related_name='%(class)s_upvoters', blank=True)
    vote_down_users = models.ManyToManyField(
        "users.User", verbose_name='Downvoting Users', related_name='%(class)s_downvoters', blank=True)

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

    def got_voted(self, user, action):
        # remove user from voters
        if self.vote_up_users.filter(id=user.id).exists():
            self.vote_up_users.remove(user)
            self.score_up(reverse=True)
            self.votes -= 1

        if self.vote_down_users.filter(id=user.id).exists():
            self.vote_down_users.remove(user)
            self.score_down(reverse=True)
            self.votes += 1

        if action == '1':
            self.vote_up_users.add(user)
            self.score_up()
            self.votes += 1
        elif action == '-1':
            self.vote_down_users.add(user)
            self.score_down()
            self.votes -= 1
        elif action == '0':
            pass
        else:
            raise ValueError('vote is invalid')

        self.save()

    def vote_of(self, user):
        if user in self.vote_up_users.all():
            return 1
        if user in self.vote_down_users.all():
            return -1
        return 0

    def voting_info(self, user):
        return {
            'votes': self.votes,
            'user': self.user.as_preview(),
            'userVote': self.vote_of(user)
        }


class Post(models.Model):
    body = models.TextField('Body', default='', max_length=10000)

    created_at = models.DateTimeField('Creation Date', auto_now_add=True)
    updated_at = models.DateTimeField('Update Date', auto_now=True)

    user = models.ForeignKey(
        'users.User', verbose_name='Owner', on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def time_info(self):
        return {
            'createdAt': str(timezone.localtime(self.created_at).replace(microsecond=0)),
            'editedAt': str(timezone.localtime(self.updated_at).replace(microsecond=0)),
        }


class Comment(Post):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    reference_object = GenericForeignKey('content_type', 'object_id')

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


class Question(Post, VotedPostMixin):
    title = models.CharField('Title', max_length=200)
    tags = models.ManyToManyField(Tag, verbose_name='Tags', blank=True)

    answer_count = models.IntegerField('Number of Answers', default=0)
    comments = GenericRelation(Comment)

    images = GenericRelation(ImageAttach)
    documents = GenericRelation(DocumentAttach)

    objects = QuestionManager

    upvote_reward = 10
    downvote_penalty = 0

    def __str__(self):
        return '%d: %s' % (self.id, self.title)

    def save(self, *args, **kwargs):
        self.answer_count = self.answer_set.count()
        return super().save(*args, **kwargs)

    def is_answered(self):
        return self.answer_count != 0

    def as_preview(self, user):
        return {**self.time_info(), **self.voting_info(user), **{
            'id': str(self.id),
            'title': self.title,
            'answers': self.answer_count,
            'comments': self.comments.count(),
            'tagIds': list(str(tag.id) for tag in self.tags.all()),
        }}

    def as_detailed(self, user):
        return {**self.as_preview(user), **{
            'body': self.body,
            'answers': list(answer.as_detailed(user) for answer in self.answer_set.all()),
            'comments': list(comment.as_preview() for comment in self.comments.all()),
            'images': list(image.file.as_preview() for image in self.images.all()),
            'documents': list(document.file.as_preview() for document in self.documents.all()),
        }}


class Answer(Post, VotedPostMixin):
    question = models.ForeignKey(
        Question, verbose_name='Question', on_delete=models.CASCADE)

    comments = GenericRelation(Comment)

    images = GenericRelation(ImageAttach)
    documents = GenericRelation(DocumentAttach)

    upvote_reward = 10
    downvote_penalty = 0

    def __str__(self):
        return "Answer from %s" % self.user

    def as_preview(self, user):
        return {**self.time_info(), **self.voting_info(user), **{
            'id': str(self.id),
            'body': self.body,
        }}

    def as_detailed(self, user):
        return {**self.as_preview(user), **{
            'comments': list(comment.as_preview() for comment in self.comments.all()),
            'images': list(image.file.as_preview() for image in self.images.all()),
            'documents': list(document.as_preview() for document in self.documents.all()),
        }}
