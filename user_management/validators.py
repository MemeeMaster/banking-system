import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class GenericPasswordValidator:
    def __init__(self, regexp, error_code, error_message):
        self.regexp = regexp
        self.error_code = error_code
        self.error_message = error_message

    def validate(self, password, user=None):
        if not re.findall(self.regexp, password):
            raise ValidationError(
                _(self.error_message),
                code=self.error_code,
            )
