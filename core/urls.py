from django.urls import path
from . import views

urlpatterns = [
    # Admin URLs
    path('dashboard/admin', views.admin_dashboard, name='admin_dashboard'),

    # Patient URLs
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    # path('patients/create/', views.patient_create, name='patient_create'),
    # path('patients/<int:pk>/edit/', views.patient_update, name='patient_update'),
    # path('patients/<int:patient_id>/records/', views.MedicalRecordListView, name='medical_record_list'),
    # path('patients/<int:patient_id>/records/<int:pk>/', views.MedicalRecordDetailView, name='medical_record_detail'),
    # path('patients/<int:patient_id>/records/create/', views.MedicalRecordCreateView, name='medical_record_create'),
    # path('patients/<int:patient_id>/records/<int:pk>/update/', views.MedicalRecordUpdateView, name='medical_record_update'),

    # Appointment URLs
    path('appointments/', views.appointment_list, name='appointment_list'),
    # path('appointments/create/', views.appointment_create, name='appointment_create'),

    # Doctor URLs
    path('dashboard/doctors/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctors/', views.doctors_list, name='doctor_list'),
    path('doctors/<int:pk>/', views.doctor_details, name='doctor_details'),
    # path('doctors/add/', views.DoctorCreateView, name='doctor_add'),
    # path('doctors/<int:pk>/edit/', views.DoctorUpdateView, name='doctor_edit'),
    # path('doctors/<int:pk>/delete/', views.DoctorDeleteView, name='doctor_delete'),

    # Medical Record URLs
    path('medical-records/', views.medical_record_list, name='medical_record_list'),
    path('medical-records/<int:id>/', views.medical_record_detail, name='medical_record_detail'),

   


]
