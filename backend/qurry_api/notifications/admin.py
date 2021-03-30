from django.contrib import admin

from notifications.models import Notification, Subscription

admin.site.register(Subscription)
admin.site.register(Notification)
