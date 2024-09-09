from django.urls import path
from .views import dashboard,patient,doctor,medical_record,appointments

'''
url patterns for the core app, these urls are used to navigate through the application
'''
urlpatterns = [
   
    # Admin URLs
    path('dashboard/admin', dashboard.admin_view.as_view(), name='admin_dashboard'),

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
    path('dashboard/doctors/', doctor.doctor_dashboard, name='doctor_dashboard'),
    path('doctors/', doctor.doctors_list, name='doctor_list'),
    path('doctors/<int:pk>/', doctor.doctor_details, name='doctor_details'),
    path('doctors/create/', doctor.create_doctor, name='create_doctor'),
    path('doctors/update/<int:doctor_id>/', doctor.update_doctor, name='update_doctor'),
    path('doctors/delete/<int:doctor_id>/', doctor.delete_doctor, name='delete_doctor'),

    # Medical Record URLs
    path('medical-records/', medical_record.medical_record_list, name='medical_record_list'),
    path('medical-records/<int:id>/', medical_record.medical_record_detail, name='medical_record_detail'),
    path('medical-records/create/', medical_record.create_medical_record, name='create_medical_record'),
    path('medical-records/update/<int:id>/', medical_record.update_medical_record, name='update_medical_record'),
    path('medical-records/delete/<int:id>/', medical_record.delete_medical_record, name='delete_medical_record'),

]
