from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Patient, Appointment
from django.shortcuts import render
# from .forms import PatientForm, AppointmentForm

# Redirect to the appropriate dashboard based on user type
def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Admin-specific dashboard logic
    return render(request, 'core/admin_dashboard.html')

@login_required
@user_passes_test(is_admin)
def admin_doctor_management(request):
    # Logic to manage doctors
    return render(request, 'core/admin_doctor_management.html')

def is_doctor(user):
    return user.is_authenticated and hasattr(user, 'is_doctor') and user.is_doctor

@login_required
@user_passes_test(is_doctor)
def doctor_dashboard(request):
    # Doctor-specific dashboard logic
    return render(request, 'core/doctor_dashboard.html')

@login_required
@user_passes_test(is_doctor)
def doctor_appointment_management(request):
    # Logic to manage appointments by doctor
    return render(request, 'core/doctor_appointment_management.html')



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
    return render(request, 'core/appointments/appointment_list.html', {'appointments': appointments})

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
