from django.contrib import admin
from qurry_api.decorators import admin_thumbnail

from .models import Document, Image


@admin.register(Image)
@admin.register(Document)
@admin_thumbnail('src')
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    readonly_fields = ('id',)
