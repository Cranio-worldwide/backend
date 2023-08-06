from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(data):
    if data > timezone.now().year:
        raise ValidationError(
            'Year cannot be more than current.'
        )
    if data <= timezone.now().year - 100:
        raise ValidationError(
            f'Year cannot be less than {timezone.now().year - 100}'
        )
