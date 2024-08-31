from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Patient, Appointment
# from .forms import PatientForm, AppointmentForm

# Patient Views

@login_required
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'core/patients/patient_list.html', {'patients': patients})

@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'core/patients/patient_details.html', {'patient': patient})

# @login_required
# def patient_create(request):
#     if request.method == 'POST':
#         form = PatientForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('patient_list')
#     else:
#         form = PatientForm()
#     return render(request, 'core/patient_form.html', {'form': form, 'title': 'Create Patient'})

# @login_required
# def patient_update(request, pk):
#     patient = get_object_or_404(Patient, pk=pk)
#     if request.method == 'POST':
#         form = PatientForm(request.POST, instance=patient)
#         if form.is_valid():
#             form.save()
#             return redirect('patient_detail', pk=patient.pk)
#     else:
#         form = PatientForm(instance=patient)
#     return render(request, 'core/patient_form.html', {'form': form, 'title': 'Update Patient'})

# Appointment Views

@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(doctor=request.user)
    return render(request, 'appointment_list.html', {'appointments': appointments})

# @login_required
# def appointment_create(request):
#     if request.method == 'POST':
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             appointment = form.save(commit=False)
#             appointment.doctor = request.user
#             appointment.save()
#             return redirect('appointment_list')
#     else:
#         form = AppointmentForm()
#     return render(request, 'core/appointment_form.html', {'form': form, 'title': 'Schedule Appointment'})
