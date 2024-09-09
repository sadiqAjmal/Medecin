from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Patient, Appointment, Doctor
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView,UpdateView,DeleteView
from django.urls import reverse_lazy
from datetime import datetime


class AppointmentListView(LoginRequiredMixin, ListView):
    template_name='core/appointments/appointment_list.html'
    model = Appointment
    context_object_name = 'appointments'

    def get_queryset(self):
        user = self.request.user
        if user.is_doctor:
            return Appointment.objects.filter(doctor=user.doctor)
        else : 
           return Appointment.objects.all() 


class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'core/appointments/appointment_detail.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)



class AppointmentCreateView(LoginRequiredMixin, FormView):
    template_name = 'core/appointments/appointment_form.html'
    success_url = reverse_lazy('appointment_list')

    def get(self, *args, **kwargs):
        patients = Patient.objects.all()
        doctors = Doctor.objects.all()
        
        context = {
            'patients': patients,
            'doctors': doctors
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        patient_id = request.POST.get('patient')
        doctor_id = request.POST.get('doctor')
        scheduled_at = request.POST.get('scheduled_at')

        scheduled_at = timezone.make_aware(datetime.fromisoformat(scheduled_at))

        patient = get_object_or_404(Patient, id=patient_id)
        doctor = get_object_or_404(Doctor, id=doctor_id)

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            scheduled_at=scheduled_at
        )

        messages.success(request, 'Appointment created successfully!')
        return super().form_valid(form=None)  



class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    fields = ['patient', 'doctor', 'scheduled_at']
    template_name = 'core/appointments/appointment_update_form.html'
    
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patients'] = Patient.objects.all()
        context['doctors'] = Doctor.objects.all()
        return context

    def form_valid(self, form):
        form.instance.scheduled_at = timezone.make_aware(datetime.fromisoformat(form.cleaned_data['scheduled_at']))
        response = super().form_valid(form)
        messages.success(self.request, 'Appointment updated successfully!')
        return response

    def get_success_url(self):
        return reverse_lazy('appointment_detail', kwargs={'appointment_id': self.object.id})

class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    template_name = 'core/appointments/appointment_confirm_delete.html'
    success_url = reverse_lazy('appointment_list')
    
    login_url = '/login/'

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, 'Appointment deleted successfully!')
        return response

    def get_object(self, queryset=None):
        return get_object_or_404(Appointment, pk=self.kwargs['pk'])