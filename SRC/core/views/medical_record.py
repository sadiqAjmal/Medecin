from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from core.models import Patient, Appointment, Doctor, MedicalRecord
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
from .utils import is_admin


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
