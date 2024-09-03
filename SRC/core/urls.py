from django.urls import path
from . import views

urlpatterns = [
   
    # Admin URLs
    path('dashboard/admin', views.admin_dashboard, name='admin_dashboard'),

    # Patient URLs
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/create/', views.create_patient, name='create_patient'),
    path('patients/update/<int:patient_id>/', views.update_patient, name='update_patient'),   
    path('patients/delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),

    # Appointment URLs
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/create/', views.create_appointment, name='create_appointment'),
    path('appointments/update/<int:appointment_id>/', views.update_appointment, name='update_appointment'),
    path('appointments/delete/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
     
    # Doctor URLs
    path('dashboard/doctors/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctors/', views.doctors_list, name='doctor_list'),
    path('doctors/<int:pk>/', views.doctor_details, name='doctor_details'),
    path('doctors/create/', views.create_doctor, name='create_doctor'),
    path('doctors/update/<int:doctor_id>/', views.update_doctor, name='update_doctor'),
    path('doctors/delete/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),

    # Medical Record URLs
    path('medical-records/', views.medical_record_list, name='medical_record_list'),
    path('medical-records/<int:id>/', views.medical_record_detail, name='medical_record_detail'),
    path('medical-records/create/', views.create_medical_record, name='create_medical_record'),
    path('medical-records/update/<int:id>/', views.update_medical_record, name='update_medical_record'),
    path('medical-records/delete/<int:id>/', views.delete_medical_record, name='delete_medical_record'),

]
