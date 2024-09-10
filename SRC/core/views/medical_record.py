from core.models import Patient, Appointment, Doctor, MedicalRecord
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .utils import AdminRequiredMixin

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


class MedicalRecordDeleteView(AdminRequiredMixin, DeleteView):
    """
    View for deleting a medical record.
    """
    model = MedicalRecord
    template_name = 'core/medical_records/medical_record_confirm_delete.html'
    success_url = reverse_lazy('medical_record_list')