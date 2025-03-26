from datetime import date
from django.core.exceptions import ValidationError


def validate_age(value):
    """
    Function that will block the creation and raise an error if the
    created user is younger than 15.
    """
    today = date.today()
    age = today.year - value.year - (
            (today.month, today.day) < (value.month, value.day)
    )

    if age < 15:
        raise ValidationError(
            'Vous devez avoir au moins 15 ans pour avoir un compte.'
        )
