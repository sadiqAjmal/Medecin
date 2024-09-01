from django.urls import path
from . import views

urlpatterns = [
    # Patient URLs
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    # path('patients/create/', views.patient_create, name='patient_create'),
    # path('patients/<int:pk>/edit/', views.patient_update, name='patient_update'),

    # Appointment URLs
    path('appointments/', views.appointment_list, name='appointment_list'),
    # path('appointments/create/', views.appointment_create, name='appointment_create'),
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