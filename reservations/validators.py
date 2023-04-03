from django.core.exceptions import ValidationError


def validate_number(value):

    if value < 0:
        raise ValidationError("The number should be greater than 0")
    else:
        return value
