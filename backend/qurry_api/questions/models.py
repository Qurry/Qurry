from django.db import models

class Question(models.Model):

    id = models.IntegerField('Question-ID', primary_key=True)

    title = models.CharField('Title', max_length=200)
    body = models.TextField('Body', max_length=500)
    score = models.IntegerField('Score')

    date_time = models.DateTimeField('Date & Time', auto_now=True)
    user = models.ForeignKey("users.User", verbose_name='owner', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Answer(models.Model):

    id = models.IntegerField('Answer-ID', primary_key=True)

    body = models.TextField('Body', max_length=500)
    score = models.IntegerField('Score')

    date_time = models.DateTimeField('Date & Time', auto_now=True)
    user = models.ForeignKey("users.User", verbose_name='owner', on_delete=models.CASCADE)

