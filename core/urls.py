from django.urls import path
from . import views
from .views import DoctorListView, DoctorDetailView, DoctorCreateView, DoctorUpdateView, DoctorDeleteView 
from .views import MedicalRecordListView, MedicalRecordDetailView,MedicalRecordCreateView,MedicalRecordUpdateView

urlpatterns = [
    # Patient URLs
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    # path('patients/create/', views.patient_create, name='patient_create'),
    # path('patients/<int:pk>/edit/', views.patient_update, name='patient_update'),

    # Appointment URLs
    path('appointments/', views.appointment_list, name='appointment_list'),
    # path('appointments/create/', views.appointment_create, name='appointment_create'),

    path('doctors/', views.DoctorListView, name='doctor-list'),
    path('doctors/<int:pk>/', views.DoctorDetailView, name='doctor_detail'),
    path('doctors/add/', views.DoctorCreateView, name='doctor_add'),
    path('doctors/<int:pk>/edit/', views.DoctorUpdateView, name='doctor_edit'),
    path('doctors/<int:pk>/delete/', views.DoctorDeleteView, name='doctor_delete'),

    path('patients/<int:patient_id>/records/', views.MedicalRecordListView, name='medical_record_list'),
    path('patients/<int:patient_id>/records/<int:pk>/', views.MedicalRecordDetailView, name='medical_record_detail'),
    path('patients/<int:patient_id>/records/create/', views.MedicalRecordCreateView, name='medical_record_create'),
    path('patients/<int:patient_id>/records/<int:pk>/update/', views.MedicalRecordUpdateView, name='medical_record_update'),

]

'''
urlpatterns = [
    # Admin URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/doctors/', views.admin_doctor_management, name='admin_doctor_management'),
    # Add more admin URLs

    # Doctor URLs
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/appointments/', views.doctor_appointment_management, name='doctor_appointments'),
    # Add more doctor URLs
]
'''