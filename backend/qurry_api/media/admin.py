from django.contrib import admin

from .models import Image, Document


class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'src', 'description',)


admin.site.register(Image, FileAdmin)
admin.site.register(Document, FileAdmin)
