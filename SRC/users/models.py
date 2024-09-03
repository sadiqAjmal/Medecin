from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
