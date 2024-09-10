from django.shortcuts import get_object_or_404
from django.contrib import messages
from core.models import Appointment, Doctor, Patient
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django import forms
from django.core.cache import cache

class AppointmentListView(LoginRequiredMixin, ListView):
    """
    View for listing appointments with pagination.
    """
    template_name = 'core/appointments/appointment_list.html'
    model = Appointment
    context_object_name = 'appointments'
    paginate_by = 5  # Set the number of appointments per page

    def get_queryset(self):
        """
        Get the queryset for the view.
        """
        user = self.request.user
        if user.is_doctor:
            cache_key = f"doctor_appointments_{user.doctor.id}"
            appointments = cache.get(cache_key)
            if not appointments:
                appointments = Appointment.objects.filter(doctor=user.doctor)
                cache.set(cache_key, appointments)
            return appointments
        else:
            return Appointment.objects.all()

    def get_context_data(self, **kwargs):
        """
        Add pagination data to the context.
        """
        context = super().get_context_data(**kwargs)
        print(context)
        return context
    
class AppointmentDetailView(LoginRequiredMixin, DetailView):
    """
    View for displaying appointment details.
    """
    model = Appointment
    template_name = 'core/appointments/appointment_detail.html'

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view.
        """
        return super().get_context_data(**kwargs)


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new appointment.
    """
    template_name = 'core/appointments/appointment_form.html'
    model = Appointment
    fields = ['patient', 'doctor', 'scheduled_at']
    success_url = reverse_lazy('appointment_list')

    def get_form(self, form_class=None):
        """
        Get the form for the view.
        """
        form = super().get_form(form_class)
        form.fields['scheduled_at'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        form.fields['scheduled_at'].input_formats = ['%Y-%m-%dT%H:%M']  # Adjust input format for datetime-local
        return form

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view.
        """
        context = super().get_context_data(**kwargs)
        context['patients'] = Patient.objects.all()
        context['doctors'] = Doctor.objects.all()
        return context

    def form_valid(self, form):
        """
        Validate the form and save the appointment.
        """
        # Check if the 'scheduled_at' is not already a timezone-aware datetime object
        if not timezone.is_aware(form.cleaned_data['scheduled_at']):
            form.instance.scheduled_at = timezone.make_aware(form.cleaned_data['scheduled_at'])
        
        response = super().form_valid(form)
        messages.success(self.request, 'Appointment created successfully!')
        cache.clear()  # Clear cache after creating a new appointment
        return response


class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating an existing appointment.
    """
    model = Appointment
    fields = ['patient', 'doctor', 'scheduled_at']
    template_name = 'core/appointments/appointment_update_form.html'
    success_url = reverse_lazy('appointment_list')

    def get_form(self, form_class=None):
        """
        Get the form for the view.
        """
        form = super().get_form(form_class)
        form.fields['scheduled_at'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        form.fields['scheduled_at'].input_formats = ['%Y-%m-%dT%H:%M']  # Adjust input format for datetime-local
        return form

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view.
        """
        context = super().get_context_data(**kwargs)
        context['patients'] = Patient.objects.all()
        context['doctors'] = Doctor.objects.all()
        return context

    def form_valid(self, form):
        """
        Validate the form and save the updated appointment.
        """
        form.instance.scheduled_at = timezone.make_aware(datetime.fromisoformat(form.cleaned_data['scheduled_at']))
        response = super().form_valid(form)
        messages.success(self.request, 'Appointment updated successfully!')
        cache.clear()  # Clear cache after updating an appointment
        return response


class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting an appointment.
    """
    model = Appointment
    template_name = 'core/appointments/appointment_confirm_delete.html'
    success_url = reverse_lazy('appointment_list')

    def delete(self, request, *args, **kwargs):
        """
        Delete the appointment and display success message.
        """
        response = super().delete(request, *args, **kwargs)
        messages.success(request, 'Appointment deleted successfully!')
        cache.clear()  # Clear cache after deleting an appointment
        return response

    def get_object(self, queryset=None):
        """
        Get the appointment object for the view.
        """
        return get_object_or_404(Appointment, pk=self.kwargs['pk'])
