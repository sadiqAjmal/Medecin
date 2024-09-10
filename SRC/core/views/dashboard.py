from django.contrib.admin.models import LogEntry
from core.models import Patient, Appointment, Doctor
from django.views.generic.base import TemplateView
from .utils import AdminRequiredMixin

class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = "core/admin/admin_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patients'] = Patient.objects.all()
        context['doctors'] = Doctor.objects.all()
        context['appointments'] = Appointment.objects.all()
        context["recent_activities"] = LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')[:10]
        return context


class AdminDoctorManagementView(AdminRequiredMixin, TemplateView):
    template_name = "core/admin/admin_doctor_management.html"


class AdminDoctorDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'core/admin/admin_doctor_dashboard.html'


class AdminAppointmentManagementView(AdminRequiredMixin, TemplateView):
    template_name = "core/admin/admin_appointment_management.html"
