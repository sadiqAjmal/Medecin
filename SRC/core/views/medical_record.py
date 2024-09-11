import logging
from core.models import Patient, Appointment, Doctor, MedicalRecord
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import F

logger = logging.getLogger(__name__)

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

        logger.info(f"MedicalRecordListView accessed by user {self.request.user.id}")

        if self.request.user.is_doctor:
            queryset = MedicalRecord.objects.filter(appointment__doctor=self.request.user.doctor).order_by('-updated_at')
            logger.debug(f"Doctor-specific queryset: {queryset.count()} records")
        else:
            queryset = MedicalRecord.objects.all().order_by('-updated_at')
            logger.debug(f"General queryset: {queryset.count()} records")

        return queryset

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

    def get_context_data(self, **kwargs):
        """
        Adds additional context data to the view.
        """

        logger.info(f"MedicalRecordDetailView accessed for record ID {self.kwargs['pk']} by user {self.request.user.id}")
        return super().get_context_data(**kwargs)



class MedicalRecordDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting a medical record.
    """

    model = MedicalRecord
    template_name = 'core/medical_records/medical_record_confirm_delete.html'
    success_url = reverse_lazy('medical_record_list')

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        """
        Delete the medical record and handle any errors.
        """

        try:
            record = self.get_object()
            response = super().delete(request, *args, **kwargs)
            logger.info(f"Medical record deleted successfully with ID {record.id} by user {self.request.user.id}")
            return response
        except Exception as e:
            logger.error(f"Error deleting medical record: {e}")
            return self.render_to_response(self.get_context_data())
