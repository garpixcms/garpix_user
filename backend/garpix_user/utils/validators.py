from django.core.validators import BaseValidator
from django.utils.translation import ugettext_lazy as _


class PositiveWithInfValidator(BaseValidator):
    message = _('Ensure this value is a positive integer or -1')

    def compare(self, a, b):
        return a <= 0 and a != -1
