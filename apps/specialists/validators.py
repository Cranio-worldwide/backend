from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def validate_year(data):
    if data > timezone.now().year:
        raise ValidationError(
            _('Year should not be more than current one.')
        )
    if data <= timezone.now().year - 80:
        raise ValidationError(
            _('Year should not be less than') + f' {timezone.now().year - 100}'
        )
