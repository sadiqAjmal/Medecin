import logging
from django.db.models import Q
from core.models import Patient, Appointment, Doctor
from django.contrib.auth import get_user_model
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .utils import AdminRequiredMixin
from core.forms import DoctorForm
from django.db import transaction

# Configure logging
logger = logging.getLogger(__name__)


class DoctorDashboardView(LoginRequiredMixin, TemplateView):
    """
    View for the doctor's dashboard.
    """

    template_name = 'core/doctors/doctor_dashboard.html'

    def get_context_data(self, **kwargs):
        """
        Get the context data for the doctor's dashboard.
        """
        logger.info(f"Doctor dashboard accessed by user {self.request.user.id}")
        context = super().get_context_data(**kwargs)
        try:
            context['patients'] = Patient.objects.filter(appointment__doctor=self.request.user.doctor)
            context['appointments'] = Appointment.objects.filter(doctor=self.request.user.doctor).order_by('-scheduled_at')
            context['doctor'] = Doctor.objects.get(user=self.request.user)
            logger.debug(f"Dashboard context data: {len(context['patients'])} patients, {len(context['appointments'])} appointments")
        except Exception as e:
            logger.error(f"Error fetching context data for doctor's dashboard: {e}")

        return context


class DoctorListView(LoginRequiredMixin, ListView):
    """
    View for listing doctors.
    """

    model = Doctor
    template_name = 'core/doctors/doctors_list.html'
    context_object_name = 'doctors'
    paginate_by = 5

    def get_queryset(self):
        """
        Get the queryset of doctors based on search query and specialization filter.
        """
        query = self.request.GET.get('search_query', '')
        specialization_filter = self.request.GET.get('filter_specialization', '')
        doctors = Doctor.objects.all()
        if query:
            doctors = doctors.filter(
                Q(user__username__icontains=query) |
                Q(user__phone_number__icontains=query) |
                Q(user__email__icontains=query)
            ).order_by('user__username')
            logger.debug(f"Filtered doctors by search query: {query}")
        if specialization_filter:
            doctors = doctors.filter(specialization__icontains=specialization_filter).order_by('user__username')
            logger.debug(f"Filtered doctors by specialization: {specialization_filter}")
        return doctors

    def get_context_data(self, **kwargs):
        """
        Get the context data for the doctor list view.
        """
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search_query', '')
        context['specialization_filter'] = self.request.GET.get('filter_specialization', '')
        context['specializations'] = Doctor.objects.values_list('specialization', flat=True).distinct()
        return context


class DoctorDetailView(LoginRequiredMixin, DetailView):
    """
    View for displaying doctor details.
    """

    model = Doctor
    template_name = 'core/doctors/doctor_details.html'
    context_object_name = 'doctor'

    def get_context_data(self, **kwargs):
        """
        Get the context data for the doctor detail view.
        """
        logger.info(f"Doctor detail view accessed for doctor ID {self.kwargs['pk']}")
        return super().get_context_data(**kwargs)


User = get_user_model()

class DoctorCreateView(AdminRequiredMixin, CreateView):
    """
    View for creating a new doctor.
    """

    model = Doctor
    form_class = DoctorForm
    template_name = 'core/doctors/doctor_form.html'
    success_url = reverse_lazy('doctor_list')

    def form_valid(self, form):
        """
        Save the form data and create a new user.
        """
        try:
            with transaction.atomic():
                # Create the user instance
                user = User.objects.create(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    phone_number=form.cleaned_data['phone_number'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name']
                )
                user.set_password(form.cleaned_data['password'])
                user.is_doctor = True
                user.save()
                
                # Attach the user to the doctor instance
                form.instance.user = user
                
                # Save the doctor instance
                response = super().form_valid(form)
                logger.info(f"Doctor created successfully with user ID {user.id}")
                return response
        except Exception as e:
            logger.error(f"Error creating doctor: {e}")
            form.add_error(None, "An error occurred while creating the user. Please try again.")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        """
        Get the context data for the doctor create view.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Doctor'
        context['button_name'] = 'Create'
        return context

class DoctorUpdateView(AdminRequiredMixin, UpdateView):
    """
    View for updating a doctor's information.
    """

    model = Doctor
    form_class = DoctorForm
    template_name = 'core/doctors/doctor_form.html'
    success_url = reverse_lazy('doctor_list')

    def form_valid(self, form):
        """
        Save the form data and update the user's information.
        """
        try:
            with transaction.atomic():
                user = form.instance.user
                user.username = form.cleaned_data['username']
                user.email = form.cleaned_data['email']
                user.phone_number = form.cleaned_data['phone_number']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                
                if form.cleaned_data['password']:
                    user.set_password(form.cleaned_data['password'])
                
                user.save()
                
                response = super().form_valid(form)
                logger.info(f"Doctor updated successfully with user ID {user.id}")
                return response
        except Exception as e:
            logger.error(f"Error updating doctor: {e}")
            form.add_error(None, "An error occurred while updating the user. Please try again.")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        """
        Get the context data for the doctor update view.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Doctor'
        context['button_name'] = 'Update'
        return context

class DoctorDeleteView(AdminRequiredMixin, DeleteView):
    """
    View for deleting a doctor.
    """

    model = User
    template_name = 'core/doctors/doctor_confirm_delete.html'
    success_url = reverse_lazy('doctor_list')

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        """
        Delete the doctor and handle any errors.
        """
        try:
            user = self.get_object()
            response = super().delete(request, *args, **kwargs)
            logger.info(f"Doctor deleted successfully with user ID {user.id}")
            return response
        except Exception as e:
            logger.error(f"Error deleting doctor: {e}")
            return self.render_to_response(self.get_context_data())
