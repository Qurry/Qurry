from django.urls.conf import path, re_path

from .views import NotificationView

urlpatterns = [
    path('notifications/<int:id>/',
         NotificationView.as_view(), name='view-notification'),
    re_path(r'notifications/(((?P<query>((all)|(unread)|(status)))/)|$)',
            NotificationView.as_view(), name='get-notifications'),
]
