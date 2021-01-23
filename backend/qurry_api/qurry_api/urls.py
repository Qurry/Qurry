from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/media/', include('media.urls')),
    path('api/', include('questions.urls')),
    path('api/', include('users.urls')),
    path('api/media/', include('media.urls')),
    re_path(r'^.*', TemplateView.as_view(template_name='index.html')),
]

urlpatterns += staticfiles_urlpatterns()
