from django.db import models


class TagCategory(models.Model):
    name = models.CharField('Name', max_length=20)
    description = models.TextField('Description', blank=True, null=True)

    def __str__(self):
        return self.name

    def as_preview(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description
        }


class Tag(models.Model):

    name = models.CharField('Name', max_length=20)
    description = models.TextField('Description', blank=True, null=True)

    category = models.ForeignKey(
        TagCategory, verbose_name='Kategorie', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def category_as_string(self):
        if self.category:
            return str(self.category)
        return 'none'

    def as_preview(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'category': self.category_as_string()
        }


class Question(models.Model):

    title = models.CharField('Title', max_length=200)
    body = models.TextField('Body', max_length=10000)
    tags = models.ManyToManyField(Tag, verbose_name='Tags', blank=True)

    date_time = models.DateTimeField(
        'Date & Time', auto_now=True, blank=True, null=True)
    user = models.ForeignKey(
        "users.User", verbose_name='Owner', on_delete=models.CASCADE)

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

    def tag_id_list(self):
        return list(str(id) for id in self.tags.values_list('id', flat=True))

    def vote_of(self, user):
        if user in self.vote_up_users.all():
            return 'up'
        if user in self.vote_down_users.all():
            return 'down'
        return 'none'

    def as_preview(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'votes': self.count_votes(),
            'answers': self.count_answers(),
            'tagIds': self.tag_id_list(),
            'user': self.user.as_preview(),
            'dateTime': self.date_time
        }

    def as_detailed(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'body': self.body,
            'votes': self.count_votes(),
            'answers': list(answer.as_preview() for answer in self.answer_set.all()),
            'tagIds': self.tag_id_list(),
            'user': self.user.as_preview(),
            'dateTime': self.date_time
        }


class Answer(models.Model):
    body = models.TextField('Body', max_length=10000)

    date_time = models.DateTimeField('Date & Time', auto_now=True)

    question = models.ForeignKey(
        Question, verbose_name='Question', on_delete=models.CASCADE)
    user = models.ForeignKey(
        "users.User", verbose_name='Owner', on_delete=models.CASCADE)

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
            return 'up'
        if user in self.vote_down_users.all():
            return 'down'
        return 'none'

    def as_preview(self):
        return {
            'id': str(self.id),
            'body': self.body,
            'votes': self.count_votes(),
            'user': self.user.as_preview()
        }
