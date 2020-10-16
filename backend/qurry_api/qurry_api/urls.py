from django.contrib import admin
from django.urls import path, include

from .views import testView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/questions', include('questions.urls')),
    path('api/questions', testView)
]
