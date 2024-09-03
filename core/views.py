from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.models import LogEntry
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
    patients = Patient.objects.all()
    appointments = Appointment.objects.all()
    doctors = Doctor.objects.all()

    # Fetch recent activities from the LogEntry model
    recent_activities = LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')[:10]

    context = {
        'patients': patients,
        'appointments': appointments,
        'doctors': doctors,
        'recent_activities': recent_activities
    }

    return render(request, 'core/admin/admin_dashboard.html', context)

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
    patients = Patient.objects.filter(appointment__doctor=request.user.doctor)
    appoitments = Appointment.objects.filter(doctor=request.user.doctor)
    doctor = Doctor.objects.get(user=request.user)
    return render(request, 'core/doctors/doctor_dashboard.html', {'patients': patients, 'appointments': appoitments, 'doctor': doctor})

@login_required
def doctors_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'core/doctors/doctors_list.html', {'doctors': doctors})

@login_required
def doctor_details(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'core/doctors/doctor_details.html', {'doctor': doctor})

# Medical Record Views
@login_required
def medical_record_list(request):
    if request.user.is_doctor:
        medical_records = MedicalRecord.objects.filter(patient__appointment__doctor=request.user.doctor)
        patients = Patient.objects.filter(appointment__doctor=request.user.doctor)
        doctor = Doctor.objects.get(user=request.user)
    else:
        medical_records = MedicalRecord.objects.all()
        patients = Patient.objects.all()
        doctor = Doctor.objects.all()

    contexts = {
        'medical_records': medical_records,
        'patients': patients,
        'doctor': doctor
    }    
    return render(request, 'core/medical_records/medical_record_list.html', contexts)

# details
# @login_required
def medical_record_detail(request, id):
    # Fetch the medical record for the specific patient
    medical_record = MedicalRecord.objects.get(pk=id)

    # Render the details page with the medical record
    return render(request, 'core/medical_records/medical_record_detail.html', {'medical_record': medical_record})
