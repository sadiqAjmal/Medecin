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
