from django.urls import path

from .models import Image, Document
from .views import FileView

urlpatterns = [
    path('images/', FileView.as_view(Model=Image), name='view-images'),
    path('images/<str:id>/', FileView.as_view(Model=Image), name='view-images'),

    path('documents/', FileView.as_view(Model=Document), name='view-documents'),
    path('documents/<str:id>/', FileView.as_view(Model=Document),
         name='view-documents'),
]
