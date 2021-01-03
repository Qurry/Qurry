from django.urls import path

from .models import Image, Document
from .views import FileView

urlpatterns = [
    path('images/', FileView.as_view(Model=Image), name='view-images'),
    path('images/<str:id>/', FileView.as_view(Model=Image), name='view-images'),

    path('documetns/', FileView.as_view(Model=Document), name='view-documents'),
    path('documetns/<str:id>/', FileView.as_view(Model=Document), name='view-documents'),
]
