
from django.db import models


class Subscription(models.Model):
    question = models.ForeignKey(
        'questions.question', verbose_name='Subscribed Question', on_delete=models.CASCADE)
    user = models.ForeignKey(
        'users.user', verbose_name='Subscriber', on_delete=models.CASCADE)

    def notifiy_subscriber(self, obj):
        Notification.objects.get_or_create(
            user=self.user, question=self.question)[0].add(obj)


class Notification(models.Model):
    question = models.ForeignKey(
        'questions.question', verbose_name='Subscribed Question', on_delete=models.CASCADE)
    answers = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    updated_at = models.DateTimeField('Last Update', auto_now=True)

    user = models.ForeignKey(
        'users.user', verbose_name='Notified User', on_delete=models.CASCADE)
    is_read = models.BooleanField('Has it been read', default=False)

    class Meta:
        ordering = ('updated_at',)

    def add(self, obj):
        obj.add_to_notification(self)

        self.save()

    def as_detailed(self):
        return {
            'id': str(self.id),
            'isRead': self.is_read,
            'question': self.question.as_notification_preview(),
            'answers': self.answers,
            'comments': self.comments,
            'updatedAt': str(self.updated_at)
        }
