from datetime import date
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Basic django User class expanded to add a few custom fields
    """

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )
    can_be_contacted = models.BooleanField(
        default=False
    )
    can_data_be_shared = models.BooleanField(
        default=False
    )
    created_time = models.DateTimeField(
        auto_now_add=True
    )

    def clean(self):
        """
        Function that will inherit from its parents AbstractUser.clean().
        It adds a verification condition when creating a non-staff user, and
        raise an error if the created user is younger than 15.
        """
        super().clean()
        if not self.date_of_birth:
            raise ValidationError(
                "La date de naissance est requise pour les utilisateurs "
                "non-staff"
            )
        dob = self.date_of_birth
        today = date.today()
        age = today.year - dob.year - (
                (today.month, today.day) < (dob.month, dob.day)
        )

        if age < 15:
            raise ValidationError(
                'Vous devez avoir au moins 15 ans pour avoir un compte.'
            )
