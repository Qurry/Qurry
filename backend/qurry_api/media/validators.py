from django.core.exceptions import ValidationError

IMAGE_MEGABYTE_LIMIT = 5.0
DOCUMENT_MEGABYTE_LIMIT = 20.0


def validate_image_size(file_obj):
    filesize = file_obj.file.size

    if filesize > IMAGE_MEGABYTE_LIMIT * 1024 * 1024:
        raise ValidationError("Max image size is %sMB" % str(IMAGE_MEGABYTE_LIMIT))


def validate_document_size(file_obj):
    filesize = file_obj.file.size

    if filesize > DOCUMENT_MEGABYTE_LIMIT * 1024 * 1024:
        raise ValidationError("Max document size is %sMB" % str(DOCUMENT_MEGABYTE_LIMIT))
