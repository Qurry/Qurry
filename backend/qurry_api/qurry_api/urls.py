from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/media/', include('media.urls')),
    path('api/', include('questions.urls')),
    path('api/', include('notifications.urls')),
    path('api/', include('users.urls')),
    re_path(r'^.*', TemplateView.as_view(template_name='index.html'), name='home'),
]

urlpatterns += staticfiles_urlpatterns()
