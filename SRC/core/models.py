from django.db import models
from django.contrib.auth.models import User
from users.models import User

'''
Patient model is used to store the details of the patient
- user: reference to the User model
- date_of_birth: date of birth of the, etc
'''
class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    # Correct reference to User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'is_patient': True})
  
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    '''
    __str__ method is used to return the string representation of the object
    '''
    def __str__(self):
        return self.user.username 
    
    def details(self):    
        return f'{self.user.username} ({self.get_gender_display()}), born on {self.date_of_birth.strftime("%b %d, %Y")}'

'''
Doctor model is used to store the details of the doctor
- user: reference to the User model
- specialization: specialization of the doctor
'''

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'is_doctor': True})
    specialization = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    '''
    details method is used to return the details of the doctor
    '''
    def details(self):    
        return f"Doctor name is {self.user.first_name} with specialization of {self.specialization}"

'''
MedicalRecord model is used to store the medical record of the patient
- patient: reference to the Patient model
- doctor: reference to the Doctor model
- appointment: reference to the Appointment model
- diagnosis: diagnosis of the patient
- treatment: treatment of the patient
- notes: notes of the patient
- report: report of the patient
'''
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

    '''
    short_description method is used to return the short description of the diagnosis
    '''
    def short_description(self):
        return f"{self.diagnosis[:50]}..."  

'''
Appointment model is used to store the appointment of the patient
- patient: reference to the Patient model
- doctor: reference to the Doctor model
- scheduled_at: scheduled date and time of the appointment
'''
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment with {self.doctor} for {self.patient} on {self.scheduled_at}"