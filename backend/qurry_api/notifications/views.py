from django.http import Http404
from django.http.response import JsonResponse
from django.views import View
from qurry_api.decorators import authenticate_user


class NotificationView(View):

    @authenticate_user
    def all(self, request, *args, **kwargs):
        notifications = self.user.notifications.all()
        return JsonResponse({
            'count': notifications.count(),
            'notifications': list(notification.as_detailed() for notification in notifications)
        })

    @authenticate_user
    def status(self, request, *args, **kwargs):
        notifications = self.user.notifications.filter(is_read=False)
        return JsonResponse({'count': notifications.count()})

    @authenticate_user
    def unread(self, request, *args, **kwargs):
        notifications = self.user.notifications.filter(is_read=False)
        return JsonResponse({
            'count': notifications.count(),
            'notifications': list(notification.as_detailed() for notification in notifications)
        })
