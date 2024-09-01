from django.contrib import admin
from .models import Patient, Appointment, Doctor, MedicalRecord

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'date_of_birth', 'gender', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'phone_number')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'scheduled_at', 'created_at', 'updated_at')
    search_fields = ('patient__name', 'doctor__username')
    list_filter = ['scheduled_at']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'specialization', 'created_at', 'updated_at')
    search_fields = ('name',) 
    list_filter = ('specialization',)  

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'diagnosis', 'treatment', 'date', 'created_at', 'updated_at')
    search_fields = ('patient__name', 'diagnosis', 'treatment')
    list_filter = ('date')