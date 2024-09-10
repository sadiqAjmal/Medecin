from django.urls import path
from .views import dashboard,patient,doctor,medical_record,appointments

'''
url patterns for the core app, these urls are used to navigate through the application
'''
urlpatterns = [
   
    # Admin URLs
    path('dashboard/admin', dashboard.AdminDashboardView.as_view(), name='admin_dashboard'),

    # Patient URLs
    path('patients/', patient.patient_list, name='patient_list'),
    path('patients/<int:pk>/', patient.patient_detail, name='patient_detail'),
    path('patients/create/', patient.create_patient, name='create_patient'),
    path('patients/update/<int:patient_id>/', patient.update_patient, name='update_patient'),   
    path('patients/delete/<int:patient_id>/', patient.delete_patient, name='delete_patient'),

    # Appointment URLs
    path('appointments/', appointments.appointment_list, name='appointment_list'),
    path('appointments/<int:appointment_id>/', appointments.appointment_detail, name='appointment_detail'),
    path('appointments/create/', appointments.create_appointment, name='create_appointment'),
    path('appointments/update/<int:appointment_id>/', appointments.update_appointment, name='update_appointment'),
    path('appointments/delete/<int:appointment_id>/', appointments.delete_appointment, name='delete_appointment'),
     
    # Doctor URLs
    path('dashboard/doctors/', doctor.DoctorDashboardView.as_view(), name='doctor_dashboard'),
    path('doctors/', doctor.DoctorListView.as_view(), name='doctor_list'),
    path('doctors/<int:pk>/', doctor.DoctorDetailView.as_view(), name='doctor_details'),
    path('doctors/create/', doctor.DoctorCreateView.as_view(), name='create_doctor'),
    path('doctors/update/<int:pk>/', doctor.DoctorUpdateView.as_view(), name='update_doctor'),
    path('doctors/delete/<int:pk>/', doctor.DoctorDeleteView.as_view(), name='delete_doctor'),

    # Medical Record URLs
    path('medical-records/', medical_record.MedicalRecordListView.as_view(), name='medical_record_list'),
    path('medical-records/<int:pk>/', medical_record.MedicalRecordDetailView.as_view(), name='medical_record_detail'),
    path('medical-records/create/', medical_record.MedicalRecordCreateView.as_view(), name='create_medical_record'),
    path('medical-records/update/<int:pk>/', medical_record.MedicalRecordUpdateView.as_view(), name='update_medical_record'),
    path('medical-records/delete/<int:pk>/', medical_record.MedicalRecordDeleteView.as_view(), name='delete_medical_record'),

]
