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

class MedicalRecordCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new medical record.
    """
    model = MedicalRecord
    fields = ['appointment', 'diagnosis', 'treatment', 'notes', 'report']
    template_name = 'core/medical_records/medical_record_form.html'
    success_url = reverse_lazy('medical_record_list')

    def get_context_data(self, **kwargs):
        """
        Adds additional context data to the view.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Medical Record'
        context['button_name'] = 'Create'
        return context

    def get_form(self, form_class=None):
        """
        Override to filter appointments based on user type.
        """
        form = super().get_form(form_class)
        user = self.request.user

        if user.is_superuser:
            form.fields['appointment'].queryset = Appointment.objects.all()
        elif user.is_doctor:
            form.fields['appointment'].queryset = Appointment.objects.filter(doctor=user.doctor)
        else:
            form.fields['appointment'].queryset = Appointment.objects.none()

        return form

    def form_valid(self, form):
        """
        Validate the form and save the medical record within a transaction.
        """
        try:
            with transaction.atomic():
                form.instance.patient = form.instance.appointment.patient

                response = super().form_valid(form)
                logger.info(f"Medical record created successfully with ID {self.object.id} by user {self.request.user.id}")
                return response
        except Exception as e:
            logger.error(f"Error creating medical record: {e}", exc_info=True)
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
                logger.info(f"Medical record updated successfully with ID {self.object.id} by user {self.request.user.id}")
                return response
        except Exception as e:
            logger.error(f"Error updating medical record: {e}")
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
