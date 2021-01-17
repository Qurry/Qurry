import re

from django.core import validators
from django.utils.deconstruct import deconstructible

@deconstructible
class HPIEmailValidator(validators.RegexValidator):
    regex = r'^[\w\.-]*@([\w\.-]+\.)?(hpi\.de|hpi\.uni-potsdam\.de)\Z'
    message = 'You have to provide a valid HPI email address'
    flags = re.ASCII
