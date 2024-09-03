from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.models import LogEntry
from .models import Patient, Appointment, Doctor, MedicalRecord
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Q
from datetime import datetime
from django.utils import timezone
from django.core.files.storage import FileSystemStorage


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

@login_required
def create_patient(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        date_of_birth = request.POST.get('date_of_birth')  # Use snake_case for consistency
        gender = request.POST.get('gender')
        password = request.POST.get('password')

        # Create User object
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone_number=phone_number
        )

        # Create Patient object
        Patient.objects.create(
            user=user,
            date_of_birth=date_of_birth,
            gender=gender
        )

        return redirect('patient_list')
    
    return render(request, 'core/patients/patient_form.html')


@login_required
def update_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        patient.user.username = request.POST.get('username')
        patient.user.email = request.POST.get('email')
        patient.user.phone_number = request.POST.get('phone_number')
        patient.gender = request.POST.get('gender')
        patient.date_of_birth = request.POST.get('date_of_birth')
     
        patient.user.save()
        patient.save()
        
        messages.success(request, 'Patient updated successfully!')
        return redirect('patient_list')

    context = {
        'patient': patient,
    }
    return render(request, 'core/patients/update_patient_form.html', context)



@login_required
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        # Deleting the related User will automatically delete the Patient due to CASCADE
        patient.user.delete()  
        messages.success(request, 'Patient deleted successfully!')
        return redirect('patient_list')  
    
    return render(request, 'core/patients/patient_confirm_delete.html', {'patient': patient})







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
def appointment_detail(request, appointment_id):
    # Fetch the appointment based on the provided ID
    appointment = get_object_or_404(Appointment, id=appointment_id)
    # Pass the appointment object to the template
    context = {
        'appointment': appointment,
    }
    return render(request, 'core/appointments/appointment_detail.html', context)



@login_required
def create_appointment(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        doctor_id = request.POST.get('doctor')
        scheduled_at = request.POST.get('scheduled_at')
        
        # Convert scheduled_at to a datetime object
        scheduled_at = timezone.make_aware(datetime.fromisoformat(scheduled_at))

        patient = get_object_or_404(Patient, id=patient_id)
        doctor = get_object_or_404(Doctor, id=doctor_id)
        
        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            scheduled_at=scheduled_at
        )
        
        messages.success(request, 'Appointment created successfully!')
        return redirect('appointment_list')
    
    # Get available patients and doctors for the form
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    
    context = {
        'patients': patients,
        'doctors': doctors
    }
    return render(request, 'core/appointments/appointment_form.html', context)




@login_required
def update_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        doctor_id = request.POST.get('doctor')
        scheduled_at = request.POST.get('scheduled_at')
        
        # Convert scheduled_at to a datetime object
        scheduled_at = timezone.make_aware(datetime.fromisoformat(scheduled_at))
        
        appointment.patient = get_object_or_404(Patient, id=patient_id)
        appointment.doctor = get_object_or_404(Doctor, id=doctor_id)
        appointment.scheduled_at = scheduled_at
        
        appointment.save()
        
        messages.success(request, 'Appointment updated successfully!')
        return redirect('appointment_detail', appointment_id=appointment.id)
    
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    
    context = {
        'appointment': appointment,
        'patients': patients,
        'doctors': doctors
    }
    return render(request, 'core/appointments/appointment_update_form.html', context)


@login_required
def delete_appointment(request, appointment_id):
    # Fetch the appointment based on the provided ID
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment deleted successfully!')
        return redirect('appointment_list')  # Redirect to the appointment list view
    
    return render(request, 'core/appointments/appointment_confirm_delete.html', {'appointment': appointment})




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

@login_required
def medical_record_detail(request, id):
    # Fetch the medical record for the specific patient
    medical_record = MedicalRecord.objects.get(pk=id)
    # Render the details page with the medical record
    return render(request, 'core/medical_records/medical_record_detail.html', {'medical_record': medical_record})





@login_required
def create_medical_record(request):
    if request.method == 'POST':
        patient = request.POST.get('patient')
        doctor = request.POST.get('doctor')
        appointment = request.POST.get('appointment')
        diagnosis = request.POST.get('diagnosis')
        treatment = request.POST.get('treatment')
        notes = request.POST.get('notes')
        report = request.FILES.get('report')  # Handle file uploads

        # Create and save the MedicalRecord
        MedicalRecord.objects.create(
            patient_id=patient,
            doctor_id=doctor,
            appointment_id=appointment,
            diagnosis=diagnosis,
            treatment=treatment,
            notes=notes,
            report=report
        )
        return redirect('medical_record_list')  # Redirect to the medical records list page

    # Prepare context for the GET request
    context = {
        'patients': Patient.objects.all(),
        'doctors': Doctor.objects.all(),
        'appointments': Appointment.objects.all(),
    }
    return render(request, 'core/medical_records/medical_record_form.html', context)



@login_required
def update_medical_record(request, id):
    # Fetch the existing medical record
    medical_record = get_object_or_404(MedicalRecord, id=id)

    if request.method == 'POST':
        # Retrieve form data
        patient_id = request.POST.get('patient')
        doctor_id = request.POST.get('doctor')
        appointment_id = request.POST.get('appointment')
        diagnosis = request.POST.get('diagnosis')
        treatment = request.POST.get('treatment')
        notes = request.POST.get('notes')
        report = request.FILES.get('report')  # Handle file uploads

        # Update the medical record
        medical_record.patient_id = patient_id
        medical_record.doctor_id = doctor_id
        medical_record.appointment_id = appointment_id
        medical_record.diagnosis = diagnosis
        medical_record.treatment = treatment
        medical_record.notes = notes
        if report:
            medical_record.report = report
        medical_record.save()

        return redirect('medical_record_list')  # Redirect to the medical records list page

    # Prepare context for the GET request
    context = {
        'medical_record': medical_record,
        'patients': Patient.objects.all(),
        'doctors': Doctor.objects.all(),
        'appointments': Appointment.objects.all(),
    }
    return render(request, 'core/medical_records/medical_record_form.html', context)



@login_required
@user_passes_test(is_admin)
def delete_medical_record(request, id):
    # Fetch the medical record based on the ID
    medical_record = get_object_or_404(MedicalRecord, id=id)

    if request.method == 'POST':
        # Delete the record
        medical_record.delete()
        # Redirect to the list of medical records
        return redirect('medical_record_list')

    # Render a confirmation page
    return render(request, 'core/medical_records/medical_record_confirm_delete.html', {'medical_record': medical_record})

#Doctors Views 
@login_required
def doctor_dashboard(request):
    patients = Patient.objects.filter(appointment__doctor=request.user.doctor)
    appoitments = Appointment.objects.filter(doctor=request.user.doctor)
    doctor = Doctor.objects.get(user=request.user)
    return render(request, 'core/doctors/doctor_dashboard.html', {'patients': patients, 'appointments': appoitments, 'doctor': doctor})

@login_required
def doctors_list(request):
    query = request.GET.get('search_query', '')
    specialization_filter = request.GET.get('filter_specialization', '')

    doctors = Doctor.objects.all()
    specializations = Doctor.objects.values_list('specialization', flat=True).distinct()
    if query:
        doctors = doctors.filter(
            Q(user__username__icontains=query) |
            Q(user__phone_number__icontains=query) |
            Q(user__email__icontains=query)
        )

    if specialization_filter:
        doctors = doctors.filter(specialization__icontains=specialization_filter)

    return render(request, 'core/doctors/doctors_list.html', {
        'doctors': doctors, 
        'search_query': query, 
        'specialization_filter': specialization_filter,
        'specializations': specializations  # Pass the specializations to the template
    })



@login_required
def doctor_details(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'core/doctors/doctor_details.html', {'doctor': doctor})

User = get_user_model()

@login_required
@user_passes_test(is_admin)
def create_doctor(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        specialization = request.POST.get('specialization')
        password = request.POST.get('password')

        # Create the user and hash the password
        user = User(
            username=username,
            phone_number=phone_number,
            email=email,
        )
        user.set_password(password)  # Hash the password
        user.is_doctor = True  # Set the is_doctor attribute
        user.save()

        # Create the doctor profile
        doctor = Doctor.objects.create(
            user=user,
            
            specialization=specialization
        )

        return redirect('doctor_list')
    return render(request, 'core/doctors/doctor_form.html')


@login_required
@user_passes_test(is_admin)
def update_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    if request.method == 'POST':
        doctor.user.username = request.POST.get('username')
        doctor.user.email = request.POST.get('email')
        doctor.user.phone_number = request.POST.get('phone_number')
        doctor.specialization = request.POST.get('specialization')
     
        doctor.user.save()
        doctor.save()
        
        messages.success(request, 'Doctor updated successfully!')
        return redirect('doctor_list') 

    context = {
        'doctor': doctor,
    }
    return render(request, 'core/doctors/update_doctor_form.html', context)
    return render(request, 'core/doctors/doctor_form.html')

@login_required
@user_passes_test(is_admin)
def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    if request.method == 'POST':
        doctor.user.delete()  
        doctor.delete() 
        messages.success(request, 'Doctor deleted successfully!')
        return redirect('doctor_list')  
    
    return render(request, 'core/doctors/doctor_confirm_delete.html', {'doctor': doctor})

