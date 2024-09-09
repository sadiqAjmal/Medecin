from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from core.models import Patient
from django.contrib import messages
from django.contrib.auth import get_user_model

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
