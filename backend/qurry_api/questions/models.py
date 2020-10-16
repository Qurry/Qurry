from django.db import models

class Tag(models.Model):

    name = models.CharField('Name', max_length=20)
    description = models.TextField('Discription', blank=True, null=True)

    def __str__(self):
        return self.name


class Question(models.Model):

    title = models.CharField('Title', max_length=200)
    body = models.TextField('Body', max_length=500)
    votes = models.IntegerField('Votes')
    tags = models.ManyToManyField(Tag, verbose_name='Tags', null=True, blank=True)

    date_time = models.DateTimeField('Date & Time', auto_now=True, null=True)
    user = models.ForeignKey("users.User", verbose_name='Owner', on_delete=models.CASCADE)


    def __str__(self):
        return self.title

class Answer(models.Model):

    body = models.TextField('Body', max_length=500)
    votes = models.IntegerField('Vote')

    date_time = models.DateTimeField('Date & Time', auto_now=True)

    question = models.ForeignKey(Question, verbose_name='Question', on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", verbose_name='Owner', on_delete=models.CASCADE)