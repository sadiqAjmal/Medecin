from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Patient, Appointment, Doctor
from django.utils import timezone
from datetime import datetime


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