import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.regex_helper import _lazy_re_compile


@deconstructible
class HPIEmailValidator(validators.EmailValidator):
    domain_regex = _lazy_re_compile(
        r'(.+\.)?hpi\.de\Z',
        re.IGNORECASE)
    message = 'You have to provide a valid HPI email address like `chris.neinel@student.hpi.de`'
