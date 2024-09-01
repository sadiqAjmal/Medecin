from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Patient, Appointment, Doctor, MedicalRecord

# Utility functions
def is_admin(user):
    return user.is_authenticated and user.is_staff

def is_doctor(user):
    return user.is_authenticated and hasattr(user, 'is_doctor') and user.is_doctor

# Dashboard Views
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'core/admin_dashboard.html')

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
    patients = Patient.objects.all()
    return render(request, 'core/patients/patient_list.html', {'patients': patients})

@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'core/patients/patient_details.html', {'patient': patient})

# Appointment Views
@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(doctor=request.user)
    return render(request, 'core/appointments/appointment_list.html', {'appointments': appointments})

# Doctor Views
@login_required
@user_passes_test(is_doctor)
class DoctorListView(ListView):
    model = Doctor
    template_name = 'doctor_list.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        specialization = self.request.GET.get('specialization', '')
        if specialization:
            queryset = queryset.filter(specialization__icontains=specialization)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specializations'] = Doctor.objects.values_list('specialization', flat=True).distinct()
        return context

@login_required
@user_passes_test(is_doctor)
class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'doctor_detail.html'
    context_object_name = 'doctor'

@login_required
@user_passes_test(is_doctor)
class DoctorCreateView(CreateView):
    model = Doctor
    template_name = 'doctor_form.html'
    fields = ['name', 'email', 'phone_number', 'specialization']
    success_url = reverse_lazy('doctor_list')

@login_required
@user_passes_test(is_doctor)
class DoctorUpdateView(UpdateView):
    model = Doctor
    template_name = 'doctor_form.html'
    fields = ['name', 'email', 'phone_number', 'specialization']
    success_url = reverse_lazy('doctor_list')

@login_required
@user_passes_test(is_doctor)
class DoctorDeleteView(DeleteView):
    model = Doctor
    template_name = 'doctor_confirm_delete.html'
    success_url = reverse_lazy('doctor_list')

# Medical Record Views
@login_required
class MedicalRecordListView(ListView):
    model = MedicalRecord
    template_name = 'medical_record_list.html'
    context_object_name = 'medical_records'

    def get_queryset(self):
        patient = get_object_or_404(Patient, pk=self.kwargs['patient_id'])
        return MedicalRecord.objects.filter(patient=patient)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = get_object_or_404(Patient, pk=self.kwargs['patient_id'])
        return context

@login_required
class MedicalRecordDetailView(DetailView):
    model = MedicalRecord
    template_name = 'medical_record_detail.html'
    context_object_name = 'medical_record'

    def get_object(self):
        patient = get_object_or_404(Patient, pk=self.kwargs['patient_id'])
        return get_object_or_404(MedicalRecord, pk=self.kwargs['pk'], patient=patient)

@login_required
class MedicalRecordCreateView(CreateView):
    model = MedicalRecord
    template_name = 'medical_record_form.html'
    fields = ['diagnosis', 'treatment', 'date']

    def get_success_url(self):
        return reverse_lazy('medical_record_list', kwargs={'patient_id': self.kwargs['patient_id']})

    def form_valid(self, form):
        form.instance.patient = get_object_or_404(Patient, pk=self.kwargs['patient_id'])
        return super().form_valid(form)

@login_required
class MedicalRecordUpdateView(UpdateView):
    model = MedicalRecord
    template_name = 'medical_record_form.html'
    fields = ['diagnosis', 'treatment', 'date']

    def get_success_url(self):
        return reverse_lazy('medical_record_detail', kwargs={'patient_id': self.kwargs['patient_id'], 'pk': self.kwargs['pk']})

    def get_object(self):
        patient = get_object_or_404(Patient, pk=self.kwargs['patient_id'])
        return get_object_or_404(MedicalRecord, pk=self.kwargs['pk'], patient=patient)
