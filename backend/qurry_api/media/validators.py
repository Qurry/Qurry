from django.core.exceptions import ValidationError

MEGABYTE_LIMIT = 5.0


def validate_image_size(fieldfile_obj):
    filesize = fieldfile_obj.file.size

    if filesize > MEGABYTE_LIMIT*1024*1024:
        raise ValidationError("Max file size is %sMB" % str(MEGABYTE_LIMIT))
