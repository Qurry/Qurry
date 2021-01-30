import uuid
import sys
from PIL import Image as PIL_Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.conf import settings

from .validators import validate_image_size, validate_document_size


class File(models.Model):
    id = models.UUIDField('UUID',
                          primary_key=True, default=uuid.uuid4, editable=False,
                          )

    description = models.TextField('Description', blank=True, default='')
    uploaded_at = models.DateTimeField('Upload Date', auto_now_add=True)

    user = models.ForeignKey(
        "users.User", verbose_name='Owner', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.src)

    def delete(self):
        # to delete file on AWS S3
        self.src.delete(save=False)
        # to delete file in database
        super().delete()

    def time_info(self):
        return {
            'uploadedAt': timezone.localtime(self.uploaded_at),
        }
    
    def as_preview(self):
        return {
            'id': self.id,
            'url': self.src.url,
            'description': self.description
        }


class Image(File):
    src = models.ImageField(
        'Image', upload_to='%s/images/' % settings.STORAGE_FOLDER, validators=[validate_image_size])

    # def full_clean(self, *args, **kwargs):
    #     super(Image, self).full_clean(*args, **kwargs)
    #     self.compressImage()

    # def compressImage(self):
    #     imageTemproary = PIL_Image.open(self.src)
    #     outputIoStream = BytesIO()
    #     imageTemproary.save(outputIoStream, format='JPEG', quality=settings.COMPRESSION_IMAGE_QUALITY)
    #     outputIoStream.seek(0)
    #     self.src = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % self.src.name.split(
    #         '.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)


class Document(File):
    src = models.FileField(
        'Documet', upload_to='%s/documents/' % settings.STORAGE_FOLDER, validators=[validate_document_size])


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

    def attaches_from(self, obj):
        return obj.images


class DocumentAttach(Attach):
    file = ForeignKey(Document, on_delete=models.CASCADE)

    def attaches_from(self, obj):
        return obj.documents
