from django.urls import path, include
from rest_framework import routers

from .views import register, activate

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register', register, name='register'),
    path('activate/<str:uidb64>/<str:token>', activate, name='activate')
]

