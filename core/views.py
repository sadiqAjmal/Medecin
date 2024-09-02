from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
# from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Patient, Appointment, Doctor, MedicalRecord
from django.http import JsonResponse

# Utility functions
def is_admin(user):
    return user.is_authenticated and user.is_staff

def is_doctor(user):
    return user.is_authenticated and hasattr(user, 'is_doctor') and user.is_doctor


# Dashboard Views
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'core/admin/admin_dashboard.html')

@login_required
@user_passes_test(is_admin)
def admin_doctor_management(request):
    return render(request, 'core/admin_doctor_management.html')

@login_required
@user_passes_test(is_doctor)
def doctor_dashboard(request):
    return render(request, 'core/doctor_dashboard.html')

@login_required
@user_passes_test(is_doctor)
def doctor_appointment_management(request):
    return render(request, 'core/doctor_appointment_management.html')

# Patient Views
@login_required
def patient_list(request):
    if request.user.is_doctor:
        print(request.user.doctor.id)
        patients = Patient.objects.filter(appointment__doctor=request.user.doctor)
    else:
        patients = Patient.objects.all()
    return render(request, 'core/patients/patient_list.html', {'patients': patients})

@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'core/patients/patient_details.html', {'patient': patient})

# Appointment Views
@login_required
def appointment_list(request):
    if request.user.is_doctor:
        appointments = Appointment.objects.filter(doctor=request.user.doctor)
    else:
        appointments = Appointment.objects.all()
    # return JsonResponse({'appointments': list(appointments.values())})
    return render(request, 'core/appointments/appointment_list.html', {'appointments': appointments})


@login_required
def doctor_dashboard(request):
    return render(request, 'core/doctors/doctor_dashboard.html')

