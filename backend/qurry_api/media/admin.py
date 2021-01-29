from django.contrib import admin

from qurry_api.base import admin_thumbnail
from .models import Image, Document


@admin_thumbnail('src')
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'src', 'description',)


admin.site.register(Image, FileAdmin)
admin.site.register(Document, FileAdmin)
