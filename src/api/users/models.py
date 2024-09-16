from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import get_object_or_404

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Role field (custom string input instead of constants)
    role = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Automatically assign the 'admin' role if the user is a superuser
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)

    @classmethod
    def get_by_role(cls, role):
        return cls.objects.filter(role=role)

    @classmethod
    def get_by_id(cls, user_id):
        return get_object_or_404(cls, id=user_id)
