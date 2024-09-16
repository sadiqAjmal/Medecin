from django.db import models
from api.users.models import User
from api.appointments.models import Appointment

class MedicalRecord(models.Model):
    appointment = models.OneToOneField(Appointment, null=True, blank=True, on_delete=models.SET_NULL)
    diagnosis = models.TextField()
    treatment = models.TextField()
    notes = models.TextField()
    report = models.FileField(upload_to='medical_records/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'Record for {self.patient.name}'
