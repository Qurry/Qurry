from django.db import models


class Tag(models.Model):

    name = models.CharField('Name', max_length=20)
    description = models.TextField('Description', blank=True, null=True)

    def __str__(self):
        return self.name


class Question(models.Model):

    title = models.CharField('Title', max_length=200)
    body = models.TextField('Body', max_length=500)
    tags = models.ManyToManyField(Tag, verbose_name='Tags', blank=True)

    date_time = models.DateTimeField('Date & Time', auto_now=True, blank=True, null=True)
    user = models.ForeignKey("users.User", verbose_name='Owner', on_delete=models.CASCADE)

    vote_up_users = models.ManyToManyField("users.User", verbose_name='Users who voted up this question', related_name='question_upvotes', blank=True)
    vote_down_users = models.ManyToManyField("users.User", verbose_name='Users who voted down this question', related_name='question_downvotes', blank=True)

    def __str__(self):
        return self.title

    def count_votes(self):
        return len(self.vote_up_users.all()) -len(self.vote_down_users.all())

    def count_answers(self):
        return len(self.answer_set.all())

    def get_tag_id_list(self):
        return list(self.tags.values_list('id', flat=True))
    
    def as_preview(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'body': self.body,
            'votes': self.count_votes(),
            'anwers': self.count_answers(),
            'tagIds': self.get_tag_id_list(),
            'user': self.user.as_preview(),
            'dateTime': self.date_time
        }

    def as_detailed(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'body': self.body,
            'votes': self.count_votes(),
            'anwers': list(answer.as_preview() for answer in self.answer_set.all()),
            'tagIds': self.get_tag_id_list(),
            'user': self.user.as_preview(),
            'dateTime': self.date_time
        }

class Answer(models.Model):

    body = models.TextField('Body', max_length=500)

    date_time = models.DateTimeField('Date & Time', auto_now=True)

    question = models.ForeignKey(Question, verbose_name='Question', on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", verbose_name='Owner', on_delete=models.CASCADE)

    vote_up_users = models.ManyToManyField("users.User", verbose_name='Users who voted up this answer', related_name='answer_upvotes', blank=True)
    vote_down_users = models.ManyToManyField("users.User", verbose_name='Users who voted down this answer', related_name='answer_downvotes', blank=True)

    def __str__(self):
        return "Answer from %s"%self.user

    def count_votes(self):
        return len(self.vote_up_users.all()) -len(self.vote_down_users.all())

    def as_preview(self):
        return {
            'id': str(self.id),
            'body': self.body,
            'votes': self.count_votes(),
            'user': self.user.as_preview()
        }