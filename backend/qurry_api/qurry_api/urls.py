from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('questions.urls')),
    path('api/', include('users.urls')),
    path('api/media/', include('media.urls')),
    path('api/token/generate', TokenObtainPairView.as_view(), name='generate-token'),
    # path('api/token/refresh', TokenRefreshView.as_view(), name='refresh-token'),
    # path('api/token/discard', TokenRefreshView.as_view(), name='discard-token'),
    re_path(r'^.*', TemplateView.as_view(template_name="index.html")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
