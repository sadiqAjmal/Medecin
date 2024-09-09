from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.contrib import messages
from core.models import Patient, Appointment, Doctor
from django.contrib.auth import get_user_model
from .utils import is_admin

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