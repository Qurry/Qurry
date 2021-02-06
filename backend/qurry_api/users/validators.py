import re

from django.core import validators
from django.utils.deconstruct import deconstructible

@deconstructible
class HPIEmailValidator(validators.RegexValidator):
    regex = r'^[\w\.-]*@([\w\.-]+\.)?hpi\.de\Z'
    message = 'You have to provide a valid HPI email address like `chris.neinel@student.hpi.de`'
    flags = re.ASCII
