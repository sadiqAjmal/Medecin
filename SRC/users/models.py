from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
    
    # groups = models.ManyToManyField(
    #     Group,
    #     related_name='customuser_set',  # Update related_name to avoid conflicts
    #     blank=True,
    #     help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    #     verbose_name='groups',
    # )

    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     related_name='customuser_set',  # Update related_name to avoid conflicts
    #     blank=True,
    #     help_text='Specific permissions for this user.',
    #     verbose_name='user permissions',
    # )

