from django.http.response import Http404, JsonResponse
from qurry_api.views import BaseView

from notifications.forms import NotificationActionForm
from notifications.models import Notification


class NotificationView(BaseView):
    Model = Notification
    ActionForm = NotificationActionForm

    def status(self):
        notifications = self.user.notifications.filter(is_read=False)
        return {'count': notifications.count()}

    def unread(self):
        notifications = self.user.notifications.filter(is_read=False)
        return {
            'count': notifications.count(),
            'notifications': list(notification.as_detailed() for notification in notifications)
        }

    def all(self):
        notifications = self.user.notifications.all()
        return {
            'count': notifications.count(),
            'notifications': list(notification.as_detailed() for notification in notifications)
        }

    QUERIES_MAPPING = {
        'all': all,
        'status': status,
        'unread': unread,
    }

    def view_detailed(self, obj):
        return JsonResponse(obj.as_detailed())

    def view_list(self, **kwargs):
        return JsonResponse(self.QUERIES_MAPPING.get(kwargs.get('query', 'all'), Http404)(self))
