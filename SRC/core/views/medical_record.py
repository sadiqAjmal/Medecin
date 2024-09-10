from core.models import Patient, Appointment, Doctor, MedicalRecord
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .utils import AdminRequiredMixin
from django.db import transaction

class MedicalRecordListView(LoginRequiredMixin, ListView):
    """
    View for displaying a list of medical records.
    """
    model = MedicalRecord
    template_name = 'core/medical_records/medical_record_list.html'
    context_object_name = 'medical_records'
    paginate_by = 5

    def get_queryset(self):
        """
        Returns the queryset of medical records based on the user's role.
        """
        if self.request.user.is_doctor:
            return MedicalRecord.objects.filter(patient__appointment__doctor=self.request.user.doctor)
        return MedicalRecord.objects.all()

    def get_context_data(self, **kwargs):
        """
        Adds additional context data to the view.
        """
        context = super().get_context_data(**kwargs)
        if self.request.user.is_doctor:
            context['patients'] = Patient.objects.filter(appointment__doctor=self.request.user.doctor)
            context['doctor'] = Doctor.objects.get(user=self.request.user)
        else:
            context['patients'] = Patient.objects.all()
            context['doctor'] = Doctor.objects.all()
        return context


class MedicalRecordDetailView(LoginRequiredMixin, DetailView):
    """
    View for displaying the details of a medical record.
    """
    model = MedicalRecord
    template_name = 'core/medical_records/medical_record_detail.html'
    context_object_name = 'medical_record'


class MedicalRecordCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new medical record.
    """
    model = MedicalRecord
    fields = ['patient', 'doctor', 'appointment', 'diagnosis', 'treatment', 'notes', 'report']
    template_name = 'core/medical_records/medical_record_form.html'
    success_url = reverse_lazy('medical_record_list')

    def get_context_data(self, **kwargs):
        """
        Adds additional context data to the view.
        """
        context = super().get_context_data(**kwargs)
        context['patients'] = Patient.objects.all()
        context['doctors'] = Doctor.objects.all()
        context['appointments'] = Appointment.objects.all()
        context['title'] = 'Create Medical Record'
        context['button_name'] = 'Create'
        return context

    def form_valid(self, form):
        """
        Validate the form and save the medical record within a transaction.
        """
        try:
            with transaction.atomic():
                response = super().form_valid(form)
                return response
        except Exception as e:
            form.add_error(None, "An error occurred while creating the medical record. Please try again.")
            return self.form_invalid(form)

class MedicalRecordUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating an existing medical record.
    """
    model = MedicalRecord
    fields = ['diagnosis', 'treatment', 'notes', 'report']
    template_name = 'core/medical_records/medical_record_form.html'
    success_url = reverse_lazy('medical_record_list')

    def get_context_data(self, **kwargs):
        """
        Adds additional context data to the view.
        """
        context = super().get_context_data(**kwargs)
        context['patients'] = Patient.objects.all()
        context['doctors'] = Doctor.objects.all()
        context['appointments'] = Appointment.objects.all()
        context['title'] = 'Update Medical Record'
        context['button_name'] = 'Update'
        return context

    def form_valid(self, form):
        """
        Validate the form and save the updated medical record within a transaction.
        """
        try:
            with transaction.atomic():
                response = super().form_valid(form)                
                return response
        except Exception as e:
            form.add_error(None, "An error occurred while updating the medical record. Please try again.")
            return self.form_invalid(form)



class MedicalRecordDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting a medical record.
    """
    model = MedicalRecord
    template_name = 'core/medical_records/medical_record_confirm_delete.html'
    success_url = reverse_lazy('medical_record_list')

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        record = self.get_object()
        with transaction.atomic():
            return super().delete(request, *args, **kwargs)