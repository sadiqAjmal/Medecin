from django.contrib.auth.models import AbstractUser
from django.db import models

'''
User model is used to store the details of the user
- is_doctor: boolean field to check if the user is a doctor
- is_patient: boolean field to check if the user is a patient
- phone_number: phone number of the user
'''
class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
