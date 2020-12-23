from django.db import models
from django.conf import settings

from .validators import validate_image_size


class Image(models.Model):
    src = models.ImageField(
        'Image', upload_to='images/', validators=[validate_image_size])
    description = models.TextField('Description', blank=True, null=True)

    def __str__(self):
        return self.src
