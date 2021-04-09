from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Subscription(models.Model):
    question = models.ForeignKey(
        'questions.question', verbose_name='Subscribed Question', on_delete=models.CASCADE)
    user = models.ForeignKey(
        'users.user', verbose_name='Subscriber', on_delete=models.CASCADE)

    def notifiy_subscriber(self, obj):
        Notification.objects.create(user=self.user, content_object=obj)


class Notification(models.Model):
    created_at = models.DateTimeField('Time of Creation', auto_now_add=True)

    user = models.ForeignKey(
        'users.user', verbose_name='Notified User', on_delete=models.CASCADE)
    is_read = models.BooleanField('Has it been read', default=False)

    class Meta:
        ordering = ('created_at',)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def message(self):
        return f'{self.content_object.user} {self.content_type.model}ed your question.'

    def as_detailed(self):
        return {
            'id': str(self.id),
            'isRead': str(self.is_read).lower(),
            'message': self.message(),
            'uri': '',
            'type': str(self.content_type),
            'createdAt': str(self.created_at)
        }
