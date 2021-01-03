import uuid
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils import timezone

from .validators import validate_image_size, validate_document_size

class File(models.Model):
    id = models.UUIDField('UUID',
                          primary_key=True, default=uuid.uuid4, editable=False,
                          )

    description = models.TextField('Description', blank=True, null=True)
    uploaded_at = models.DateTimeField('Upload Date', auto_now_add=True)

    user = models.ForeignKey(
        "users.User", verbose_name='Owner', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.src)

    def time_info(self):
        return {
            'uploadedAt': timezone.localtime(self.uploaded_at),
        }


class Image(File):
    src = models.ImageField(
        'Image', upload_to='images/', validators=[validate_image_size])


class Document(File):
    src = models.FileField(
        'Documet', upload_to='documents/', validators=[validate_document_size])


class Attach(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.file)

class ImageAttach(Attach):
    file = ForeignKey(Image, on_delete=models.CASCADE)

class DocumentAttach(Attach):
    file = ForeignKey(Document, on_delete=models.CASCADE)
