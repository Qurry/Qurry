from django.urls import path

from .views import FileView
from .models import Image, Document

urlpatterns = [
    path('images/', FileView.as_view(Model=Image), name='view-images'),
    # path('images/<int:id>/', FileView.as_view(Model=Image), name='view-images'),
    
    path('documetns/', FileView.as_view(Model=Document), name='view-documents'),
    # path('documetns/<int:id>/', FileView.as_view(Model=Document), name='view-documents'),
]
