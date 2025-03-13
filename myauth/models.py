from django.contrib.auth.models import AbstractUser
from myauth.validators import validate_age
from django.db import models


class User(AbstractUser):
    date_of_birth = models.DateField(validators=[validate_age])
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
