from django.db import models
from django.contrib.auth.models import User
from users.models import CustomUser

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    # Correct reference to CustomUser model
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_patient': True})
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Assuming the name is stored in the related CustomUser model
        return self.user.username  # Or self.user.get_full_name() if you have that method in CustomUser
    
    def details(self):    
        # Assuming the name is stored in the related CustomUser model
        return f'{self.user.username} ({self.get_gender_display()}), born on {self.date_of_birth.strftime("%b %d, %Y")}'

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_doctor': True})
    phone_number = models.CharField(max_length=15)
    specialization = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def details(self):    
        return f"Doctor name is {self.user.first_name} with specialization of {self.specialization}"

class MedicalRecord(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True)
    appointment = models.ForeignKey('Appointment', on_delete=models.SET_NULL, null=True)
    diagnosis = models.TextField()
    treatment = models.TextField()
    notes = models.TextField(blank=True, null=True)
    report = models.FileField(upload_to='medical_reports/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Medical Record of {self.patient} on {self.created_at}"

    def short_description(self):
        return f"{self.diagnosis[:50]}..."  

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment with {self.doctor} for {self.patient} on {self.scheduled_at}"