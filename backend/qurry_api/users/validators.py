import re

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.regex_helper import _lazy_re_compile


class HPIEmailValidator(EmailValidator):
    domain_regex = _lazy_re_compile(
        r'(.+\.)?hpi\.de$',
        re.IGNORECASE)
    message = 'You have to provide a valid HPI email address like `chris.neinel@student.hpi.de`'


def validate_word_characters(value):
    if not _lazy_re_compile(r'^\w+$', re.IGNORECASE).match(value):
        raise ValidationError('Username should contain only word characters')
