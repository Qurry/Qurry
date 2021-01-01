from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Post(models.Model):
    body = models.TextField('Body', default='', max_length=10000)

    created_at = models.DateTimeField('Creation Date', auto_now_add=True)
    updated_at = models.DateTimeField('Update Date', auto_now=True)

    user = models.ForeignKey(
        "users.User", verbose_name='Owner', on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def time_info(self):
        return {
            'createdAt': timezone.localtime(self.created_at),
            'editedAt': timezone.localtime(self.updated_at),
        }


class Comment(Post):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    reference_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return 'comment from %s' % self.user

    def as_preview(self):
        return self.time_info() | {
            'id': str(self.id),
            'body': self.body,
            'user': self.user.as_preview()
        }

    def as_detailed(self):
        return self.as_preview() | {
            '%sId' % self.content_type.model: self.object_id,
        }


class TagCategory(models.Model):
    name = models.CharField('Name', max_length=20)
    description = models.TextField('Description', default='')

    def __str__(self):
        return self.name

    def tags_as_preview(self):
        return list(tag.as_preview() for tag in self.tag_set.all())

    def as_preview(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'tags': self.tags_as_preview()
        }


class Tag(models.Model):

    name = models.CharField('Name', max_length=20)
    description = models.TextField('Description', default='')

    def default_category():
        return TagCategory.objects.get_or_create(name='other')[0].id

    category = models.ForeignKey(
        TagCategory, verbose_name='Category', default=default_category, on_delete=models.SET_DEFAULT)

    def __str__(self):
        return self.name

    def as_preview(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
        }


class Question(Post):

    title = models.CharField('Title', max_length=200)
    tags = models.ManyToManyField(Tag, verbose_name='Tags', blank=True)

    comments = GenericRelation(Comment)

    vote_up_users = models.ManyToManyField(
        "users.User", verbose_name='Users who voted up this question', related_name='question_upvotes', blank=True)
    vote_down_users = models.ManyToManyField(
        "users.User", verbose_name='Users who voted down this question', related_name='question_downvotes', blank=True)

    def __str__(self):
        return '%d: %s' % (self.id, self.title)

    def count_votes(self):
        return self.vote_up_users.count() - self.vote_down_users.count()

    def count_answers(self):
        return self.answer_set.count()

    def count_comments(self):
        return self.comments.count()

    def tag_id_list(self):
        return list(str(id) for id in self.tags.values_list('id', flat=True))

    def vote_of(self, user):
        if user in self.vote_up_users.all():
            return 1
        if user in self.vote_down_users.all():
            return -1
        return 0

    def as_preview(self, user):
        return self.time_info() | {
            'id': str(self.id),
            'title': self.title,
            'votes': self.count_votes(),
            'answers': self.count_answers(),
            'comments': self.count_comments(),
            'tagIds': self.tag_id_list(),
            'user': self.user.as_preview(),
            'userVote': self.vote_of(user)
        }

    def as_detailed(self, user):
        return self.as_preview(user) | {
            'body': self.body,
            'answers': list(answer.as_detailed(user) for answer in self.answer_set.all()),
            'comments': list(comment.as_preview() for comment in self.comments.all()),
        }


class Answer(Post):
    question = models.ForeignKey(
        Question, verbose_name='Question', on_delete=models.CASCADE)

    comments = GenericRelation(Comment)

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
        return self.time_info() | {
            'id': str(self.id),
            'body': self.body,
            'votes': self.count_votes(),
            'user': self.user.as_preview(),
            'userVote': self.vote_of(user)
        }

    def as_detailed(self, user):
        return self.as_preview(user) | {
            'comments': list(comment.as_preview() for comment in self.comments.all())
        }
