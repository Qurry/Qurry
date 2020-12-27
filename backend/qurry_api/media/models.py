from django.db import models
from django.conf import settings

from .validators import validate_image_size, validate_document_size


class Image(models.Model):
    src = models.ImageField(
        'Image', upload_to='images/', validators=[validate_image_size])
    description = models.TextField('Description', blank=True, null=True)

    def __str__(self):
        return str(self.src)

class Document(models.Model):
    src = models.FileField(
        'Documet', upload_to='documents/', validators=[validate_document_size])
    description = models.TextField('Description', blank=True, null=True)

    def __str__(self):
        return str(self.src)
