import logging
from django.core.cache import cache
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from django.urls import reverse_lazy
from django import forms
from core.models import Appointment, Doctor, Patient
from .utils import invalidate_cache

# Configure logging
logger = logging.getLogger(__name__)

class AppointmentListView(LoginRequiredMixin, ListView):
    """
    View for listing appointments with pagination.
    """
    template_name = 'core/appointments/appointment_list.html'
    model = Appointment
    context_object_name = 'appointments'
    paginate_by = 2  # Set the number of appointments per page
    cache_timeout = 60 * 15  # Cache timeout, e.g., 15 minutes

    def get_queryset(self):
        """
        Fetch the queryset. The pagination and caching will be handled in paginate_queryset.
        """
        user = self.request.user
        if user.is_doctor:
            logger.info(f"Fetching appointments for doctor {user.doctor.id}")
            return Appointment.objects.filter(doctor=user.doctor).order_by('-scheduled_at')
        logger.info("Fetching all appointments")
        return Appointment.objects.all().order_by('-scheduled_at')

    def paginate_queryset(self, queryset, page_size):
        """
        Paginate the queryset and handle caching of each page separately.
        """
        page_number = self.request.GET.get('page', 1)
        try:
            page_number = int(page_number)
        except ValueError:
            page_number = 1
        
        user = self.request.user
        cache_key = f"appointments_page_{page_number}_{user.id}_{'doctor' if user.is_doctor else 'admin'}"
        logger.debug(f"Checking cache for key: {cache_key}")

        cached_page = cache.get(cache_key)
        if cached_page:
            logger.info(f"Cache hit for page {page_number}")
            return cached_page, cached_page.paginator, cached_page.paginator.page_range, page_number

        logger.info(f"Cache miss for page {page_number}. Fetching from database.")
        paginator = Paginator(queryset, page_size)
        page = paginator.get_page(page_number)
        
        for appointment in page.object_list:
            appointment_cache_key = f"appointment_{appointment.id}"
            cache.set(appointment_cache_key, appointment, self.cache_timeout)
        
        cache.set(cache_key, page, self.cache_timeout)
        logger.info(f"Page {page_number} cached")

        return page, paginator, paginator.page_range, page_number

    def get_context_data(self, **kwargs):
        """
        Add pagination data to the context.
        """
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        paginated_page, paginator, _, page_number = self.paginate_queryset(queryset, self.paginate_by)

        context['appointments'] = paginated_page.object_list
        context['page_obj'] = paginated_page
        context.update({
            'has_next': paginated_page.has_next(),
            'has_previous': paginated_page.has_previous(),
            'next_page_number': paginated_page.next_page_number() if paginated_page.has_next() else None,
            'previous_page_number': paginated_page.previous_page_number() if paginated_page.has_previous() else None,
            'total_pages': paginator.num_pages if paginator else 1,
            'current_page': page_number,
        })

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
        logger.debug(f"Fetching context data for appointment {self.object.pk}")
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
        form.fields['scheduled_at'].input_formats = ['%Y-%m-%dT%H:%M']
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
        Validate the form and save the appointment within a transaction.
        """
        try:
            with transaction.atomic():
                if not timezone.is_aware(form.cleaned_data['scheduled_at']):
                    form.instance.scheduled_at = timezone.make_aware(form.cleaned_data['scheduled_at'])

                response = super().form_valid(form)

                messages.success(self.request, 'Appointment created successfully!')
                logger.info(f"Appointment {form.instance.id} created by user {self.request.user.id}")

                invalidate_cache(doctor_id=form.cleaned_data['doctor'].id, appointment_id=form.instance.id)

                return response
        except Exception as e:
            logger.error(f"Error creating appointment: {e}")
            form.add_error(None, f"An error occurred while saving the appointment: {e}")
            return self.form_invalid(form)

class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating an existing appointment.
    """
    model = Appointment
    fields = ['is_completed', 'patient', 'doctor', 'scheduled_at']
    template_name = 'core/appointments/appointment_update_form.html'
    success_url = reverse_lazy('appointment_list')

    def get_form(self, form_class=None):
        """
        Get the form for the view.
        """
        form = super().get_form(form_class)
        form.fields['scheduled_at'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        form.fields['scheduled_at'].input_formats = ['%Y-%m-%dT%H:%M']
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
        Validate the form and save the updated appointment within a transaction.
        """
        try:
            with transaction.atomic():
                if not timezone.is_aware(form.cleaned_data['scheduled_at']):
                    form.instance.scheduled_at = timezone.make_aware(form.cleaned_data['scheduled_at'])

                response = super().form_valid(form)

                messages.success(self.request, 'Appointment updated successfully!')
                logger.info(f"Appointment {form.instance.id} updated by user {self.request.user.id}")

                invalidate_cache(doctor_id=form.cleaned_data['doctor'].id, appointment_id=form.instance.id)

                return response
        except Exception as e:
            logger.error(f"Error updating appointment: {e}")
            form.add_error(None, f"An error occurred while updating the appointment: {e}")
            return self.form_invalid(form)

    def get_object(self, queryset=None):
        """
        Get the object to be updated, checking the cache first.
        """
        appointment_id = self.kwargs.get('pk')
        cache_key = f"appointment_{appointment_id}"
        logger.debug(f"Fetching appointment from cache with key: {cache_key}")

        appointment = cache.get(cache_key)
        if appointment is None:
            logger.debug(f"Cache miss for appointment {appointment_id}. Fetching from database.")
            appointment = super().get_object(queryset)
            cache.set(cache_key, appointment)
        else:
            logger.info(f"Cache hit for appointment {appointment_id}")

        return appointment

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
        try:
            appointment = self.get_object()
            doctor_id = appointment.doctor.id
            appointment_id = appointment.id
            with transaction.atomic():
                response = super().delete(request, *args, **kwargs)
                messages.success(request, 'Appointment deleted successfully!')
                logger.info(f"Appointment {appointment_id} deleted by user {request.user.id}")
                invalidate_cache(appointment_id=appointment_id, doctor_id=doctor_id)
                return response
        except Exception as e:
            logger.error(f"Error deleting appointment: {e}")
            messages.error(request, f"An error occurred while deleting the appointment: {e}")
            return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """
        Get the object to be deleted, or raise a 404 if not found.
        """
        return get_object_or_404(Appointment, pk=self.kwargs['pk'])
