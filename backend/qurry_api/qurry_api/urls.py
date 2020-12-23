from django.contrib import admin
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('questions.urls')),
    path('api/', include('users.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token'),
    path('api/refresh_token/', TokenRefreshView.as_view(), name='refresh_token'),
]
