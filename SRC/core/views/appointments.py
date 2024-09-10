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
from django.db import DatabaseError, transaction
from core.forms import AppointmentFilterForm
from django.views import View
from django.shortcuts import render
from django.db.models import Count
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.cache import cache
from django.core.cache import cache
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.paginator import Paginator
from django.core.cache import cache
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import invalidate_cache_for_user


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
            return Appointment.objects.filter(doctor=user.doctor).order_by('-scheduled_at')
        return Appointment.objects.all().order_by('-scheduled_at')

    def paginate_queryset(self, queryset, page_size):
        """
        Paginate the queryset and handle caching of each page separately.
        """
        # Get the current page number from request and ensure it's an integer
        page_number = self.request.GET.get('page', 1)
        try:
            page_number = int(page_number)
        except ValueError:
            page_number = 1
        
        user = self.request.user
        cache_key = f"appointments_page_{page_number}_{user.id}_{'doctor' if user.is_doctor else 'admin'}"

        # Check cache for the specific page's data
        cached_page = cache.get(cache_key)
        if cached_page:
            return cached_page, cached_page.paginator, cached_page.paginator.page_range, page_number  # Proper structure for returning cached data

        # If not cached, paginate the queryset
        paginator = Paginator(queryset, page_size)
        page = paginator.get_page(page_number)

        # Cache the result for the current page
        cache.set(cache_key, page, self.cache_timeout)

        return page, paginator, paginator.page_range, page_number

    def get_context_data(self, **kwargs):
        """
        Add pagination data to the context.
        """
        context = super().get_context_data(**kwargs)

        # Fetch the queryset and paginate it (with caching)
        queryset = self.get_queryset()
        paginated_page, paginator, _, page_number = self.paginate_queryset(queryset, self.paginate_by)

        # Add pagination information to context
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
        Get the context data for the view with transaction handling.
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

                invalidate_cache_for_user(doctor_id=form.cleaned_data['doctor'].id)

                return response
        except Exception as e:
            form.add_error(None, f"An error occurred while saving the appointment: {e}")
            return self.form_invalid(form)


class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating an existing appointment.
    """
    model = Appointment
    fields = ['is_completed','patient', 'doctor', 'scheduled_at']
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
        Validate the form and save the updated appointment within a transaction.
        """
        try:
            with transaction.atomic():
                if not timezone.is_aware(form.cleaned_data['scheduled_at']):
                    form.instance.scheduled_at = timezone.make_aware(form.cleaned_data['scheduled_at'])

                response = super().form_valid(form)

                messages.success(self.request, 'Appointment updated successfully!')
                invalidate_cache_for_user(doctor_id=form.cleaned_data['doctor'].id)

                return response
        except Exception as e:
            form.add_error(None, f"An error occurred while updating the appointment: {e}")
            return self.form_invalid(form)


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
            with transaction.atomic():
                response = super().delete(request, *args, **kwargs)
                messages.success(request, 'Appointment deleted successfully!')
                invalidate_cache_for_user()
                return response
        except Exception as e:
            messages.error(request, f"An error occurred while deleting the appointment: {e}")
            return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(Appointment, pk=self.kwargs['pk'])
    
class AppointmentFilterView(View):
    template_name = 'core/appointments/appointment_filter_form.html'

    def get(self, request):
        form = AppointmentFilterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AppointmentFilterForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            doctor_name = form.cleaned_data['doctor_name']
            
            appointments = Appointment.objects.filter(scheduled_at__date__range=[start_date, end_date])
            
            if doctor_name:
                appointments = appointments.filter(Q(doctor__user__first_name__icontains=doctor_name)|Q(doctor__user__last_name__icontains=doctor_name))
            print(appointments)
            appointment_counts = appointments.values('scheduled_at__date').annotate(count=Count('id'), completed_count=Count('id', filter=Q(is_completed=True)), pending_count=Count('id', filter=Q(is_completed=False)))
            return render(request, 'core/appointments/appointment_filter_form.html', {'start_date':start_date, 'end_date':end_date, 'appointments': appointments, 'appointment_counts': appointment_counts,'form': form})
        return render(request, self.template_name, {'form': form})
