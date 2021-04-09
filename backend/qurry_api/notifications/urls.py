from django.urls.conf import path

from .views import NotificationView

urlpatterns = [
    path('notifications/all',
         NotificationView().all, name='view-all-notifications'),
    path('notifications/unread',
         NotificationView().unread, name='view-unread-notifications'),
    path('notifications/status',
         NotificationView().status, name='view-notification-status'),
]
