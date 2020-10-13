from django.contrib import admin
from django.urls import path

from .views import testView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/questions', testView, name='test')
]
