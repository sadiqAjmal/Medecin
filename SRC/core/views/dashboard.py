import logging
from django.contrib.admin.models import LogEntry
from core.models import Patient, Appointment, Doctor
from django.views.generic.base import TemplateView
from .utils import AdminRequiredMixin

logger = logging.getLogger(__name__)

class AdminDashboardView(AdminRequiredMixin, TemplateView):
    """
    View for the admin dashboard.

    Attributes:
        template_name (str): The name of the template to render.
    """

    template_name = "core/admin/admin_dashboard.html"

    def get_context_data(self, **kwargs):
        """
        Get the context data for the admin dashboard view.

        Returns:
            dict: The context data for the template.
        """
        logger.info(f"Admin dashboard accessed by user {self.request.user.id}")
        context = super().get_context_data(**kwargs)

        try:
            context['patients'] = Patient.objects.all()
            context['doctors'] = Doctor.objects.all()
            context['appointments'] = Appointment.objects.all()
            context["recent_activities"] = LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')[:10]
            logger.debug(f"Dashboard context data: {len(context['patients'])} patients, {len(context['doctors'])} doctors, {len(context['appointments'])} appointments")
        except Exception as e:
            logger.error(f"Error fetching context data for admin dashboard: {e}")

        return context

class AdminDoctorManagementView(AdminRequiredMixin, TemplateView):
    """
    View for managing doctors in the admin panel.

    Attributes:
        template_name (str): The name of the template to render.
    """

    template_name = "core/admin/admin_doctor_management.html"

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests and log access.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The HTTP response.
        """
        logger.info(f"Admin doctor management accessed by user {request.user.id}")
        return super().get(request, *args, **kwargs)

class AdminDoctorDashboardView(AdminRequiredMixin, TemplateView):
    """
    View for the doctor dashboard in the admin panel.

    Attributes:
        template_name (str): The name of the template to render.
    """

    template_name = 'core/admin/admin_doctor_dashboard.html'

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests and log access.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The HTTP response.
        """
        logger.info(f"Admin doctor dashboard accessed by user {request.user.id}")
        return super().get(request, *args, **kwargs)

class AdminAppointmentManagementView(AdminRequiredMixin, TemplateView):
    """
    View for managing appointments in the admin panel.

    Attributes:
        template_name (str): The name of the template to render.
    """

    template_name = "core/admin/admin_appointment_management.html"

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests and log access.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The HTTP response.
        """
        logger.info(f"Admin appointment management accessed by user {request.user.id}")
        return super().get(request, *args, **kwargs)
