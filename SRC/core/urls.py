from django.urls import path
from .views import dashboard,patient,doctor,medical_record,appointments

'''
url patterns for the core app, these urls are used to navigate through the application
'''
urlpatterns = [
   
    # Admin URLs
    path('dashboard/admin', dashboard.AdminDashboardView.as_view(), name='admin_dashboard'),

    # Patient URLs
    path('patients/', patient.PatientListView.as_view(), name='patient_list'),
    path('patients/<int:pk>/', patient.PatientDetailView.as_view(), name='patient_detail'),
    path('patients/create/', patient.PatientCreateView.as_view(), name='create_patient'),
    path('patients/update/<int:pk>/', patient.PatientUpdateView.as_view(), name='update_patient'),   
    path('patients/delete/<int:pk>/', patient.PatientDeleteView.as_view(), name='delete_patient'),

    # Appointment URLs
    path('appointments/', appointments.AppointmentListView.as_view(), name='appointment_list'),
    path('appointments/<int:pk>/', appointments.AppointmentDetailView.as_view(), name='appointment_detail'),
    path('appointments/create/', appointments.AppointmentCreateView.as_view(), name='create_appointment'),
    path('appointments/update/<int:pk>/', appointments.AppointmentUpdateView.as_view(), name='update_appointment'),
    path('appointments/delete/<int:pk>/', appointments.AppointmentDeleteView.as_view(), name='delete_appointment'),
     
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
