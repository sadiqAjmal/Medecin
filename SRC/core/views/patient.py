from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from core.models import Patient
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.views import View

from django.views.generic.edit import FormView,UpdateView,DeleteView


User = get_user_model()

class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'core/patients/patient_list.html'
    context_object_name = 'patients'
    
    def get_queryset(self):
        if self.request.user.is_doctor:
            return Patient.objects.filter(appointment__doctor=self.request.user.doctor)
        return Patient.objects.all()
    
    login_url = '/login/'

class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'core/patients/patient_details.html'
    context_object_name = 'patient'
    
    login_url = '/login/'

class PatientCreateView(LoginRequiredMixin, View):
    template_name = 'core/patients/patient_form.html'
    success_url = reverse_lazy('patient_list')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        password = request.POST.get('password')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone_number=phone_number
        )

        Patient.objects.create(
            user=user,
            date_of_birth=date_of_birth,
            gender=gender
        )

        messages.success(request, 'Patient created successfully!')
        return redirect(self.success_url)



class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    template_name = 'core/patients/update_patient_form.html'
    fields = ['date_of_birth', 'gender']
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        patient = self.get_object()
        kwargs['initial'] = {
            'username': patient.user.username,
            'email': patient.user.email,
            'phone_number': patient.user.phone_number,
            'date_of_birth': patient.date_of_birth,
            'gender': patient.gender
        }
        return kwargs

    def form_valid(self, form):
        patient = self.get_object()
        user = patient.user

        user.username = self.request.POST.get('username')
        user.email = self.request.POST.get('email')
        user.phone_number = self.request.POST.get('phone_number')
        user.save()

        patient.date_of_birth = self.request.POST.get('date_of_birth')
        patient.gender = self.request.POST.get('gender')
        patient.save()

        messages.success(self.request, 'Patient updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('patient_list')


class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = Patient
    template_name = 'core/patients/patient_confirm_delete.html'
    success_url = reverse_lazy('patient_list')

    def delete(self, request, *args, **kwargs):
        patient = self.get_object()
        patient.user.delete()
        
        messages.success(self.request, 'Patient deleted successfully!')
        return super().delete(request, *args, **kwargs)