from django.contrib import admin
from .models import Patient, Appointment, Doctor, MedicalRecord

'''
PatientAdmin class is used to display the patient model in the admin panel,
- list_display: list of fields to be displayed in the admin panel
- search_fields: list of fields to be searched in the admin panel
'''
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('date_of_birth', 'gender', 'created_at', 'updated_at')
    search_fields = ( 'email', 'phone_number')

'''
AppointmentAdmin class is used to display the appointment model in the admin panel,
- list_display: list of fields to be displayed in the admin panel
- search_fields: list of fields to be searched in the admin panel
- list_filter: list of fields to be filtered in the admin panel
'''
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'scheduled_at', 'created_at', 'updated_at')
    search_fields = ('patient__name', 'doctor__name')
    list_filter = ['scheduled_at']

'''
DoctorAdmin class is used to display the doctor model in the admin panel,
- list_display: list of fields to be displayed in the admin panel
- search_fields: list of fields to be searched in the admin panel
- list_filter: list of fields to be filtered in the admin panel
'''
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user__username','specialization', 'created_at', 'updated_at')
    search_fields = ['user__username']
    list_filter = ['specialization']  

'''
MedicalRecordAdmin class is used to display the medical record model in the admin panel,
- list_display: list of fields to be displayed in the admin panel
- search_fields: list of fields to be searched in the admin panel
- list_filter: list of fields to be filtered in the admin panel
'''
@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment', 'created_at', 'updated_at')
    search_fields = ('patient__name', 'diagnosis', 'treatment')
    list_filter = ['patient']