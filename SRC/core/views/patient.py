import logging
from core.models import Patient
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from core.forms import PatientForm
from django.views.generic.edit import UpdateView, DeleteView,CreateView
from django.db import transaction


# Configure logging
logger = logging.getLogger(__name__)

User = get_user_model()


class PatientListView(LoginRequiredMixin, ListView):
    """
    View for displaying a list of patients.
    """
    model = Patient
    template_name = 'core/patients/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 5

    def get_queryset(self):
        """
        Get the queryset for the patient list view.
        If the user is a doctor, filter the patients based on the doctor's appointments.
        Otherwise, return all patients.
        """
        logger.info(f"PatientListView accessed by user {self.request.user.id}")
        if self.request.user.is_doctor:
            queryset = Patient.objects.filter(appointment__doctor=self.request.user.doctor).order_by("user__username")
            logger.debug(f"Doctor-specific patient list: {queryset.count()} patients")
        else:
            queryset = Patient.objects.all()
            logger.debug(f"Full patient list: {queryset.count()} patients")
        return queryset

    login_url = '/login/'


class PatientDetailView(LoginRequiredMixin, DetailView):
    """
    View for displaying the details of a patient.
    """
    model = Patient
    template_name = 'core/patients/patient_details.html'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        """
        Get the context data for the patient detail view.
        """
        logger.info(f"PatientDetailView accessed for patient ID {self.kwargs['pk']} by user {self.request.user.id}")
        return super().get_context_data(**kwargs)

    login_url = '/login/'


class PatientCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new patient.
    """
    model = Patient
    form_class = PatientForm
    template_name = 'core/patients/patient_form.html'
    success_url = reverse_lazy('patient_list')

    def form_valid(self, form):
        """
        Save the patient form data and create a new user.
        """
        try:
            with transaction.atomic():
                user = User.objects.create(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    phone_number=form.cleaned_data['phone_number'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name']
                )
                user.set_password(form.cleaned_data['password'])
                user.is_patient = True
                user.save()
                form.instance.user = user
                response = super().form_valid(form)
                logger.info(f"Patient created successfully with ID {self.object.id} by user {self.request.user.id}")
                return response
        except Exception as e:
            logger.error(f"Error creating patient: {e}")
            form.add_error(None, "An error occurred while creating the user. Please try again.")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        """
        Get the context data for the patient create view.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Patient'
        context['button_name'] = 'Create'
        return context


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating an existing patient.
    """
    model = Patient
    form_class = PatientForm
    template_name = 'core/patients/patient_form.html'
    success_url = reverse_lazy('patient_list')

    def form_valid(self, form):
        """
        Save the updated patient form data and update the associated user.
        """
        try:
            user = form.instance.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.phone_number = form.cleaned_data['phone_number']
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            user.save()
            response = super().form_valid(form)
            logger.info(f"Patient updated successfully with ID {self.object.id} by user {self.request.user.id}")
            return response
        except Exception as e:
            logger.error(f"Error updating patient: {e}")
            form.add_error(None, "An error occurred while updating the user. Please try again.")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        """
        Get the context data for the patient update view.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Patient'
        context['button_name'] = 'Update'
        return context


class PatientDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting a patient.
    """
    model = User
    template_name = 'core/patients/patient_confirm_delete.html'
    success_url = reverse_lazy('patient_list')

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        """
        Delete the patient and associated user.
        """
        try:
            user = self.get_object()
            response = super().delete(request, *args, **kwargs)
            logger.info(f"Patient deleted successfully with ID {user.id} by user {self.request.user.id}")
            return response
        except Exception as e:
            logger.error(f"Error deleting patient: {e}")
            messages.error(request, "An error occurred while deleting the patient.")
            return self.render_to_response(self.get_context_data())
