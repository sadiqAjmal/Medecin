from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.models import LogEntry
from core.models import Patient, Appointment, Doctor
from django.contrib import messages
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import is_admin,is_doctor

class admin_view(LoginRequiredMixin,TemplateView):
    template_name="core/admin/admin_dashboard.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patients'] = Patient.objects.all()
        context['doctors'] = Doctor.objects.all()
        context['appointments'] = Appointment.objects.all()
        context["recent_activities"]=LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')[:10]
        return context

@login_required
@user_passes_test(is_admin)
def admin_doctor_management(request):
    return render(request, 'core/admin_doctor_management.html')

@login_required
@user_passes_test(is_doctor)
def doctor_dashboard(request):
    return render(request, 'core/doctor_dashboard.html')

@login_required
@user_passes_test(is_doctor)
def doctor_appointment_management(request):
    return render(request, 'core/doctor_appointment_management.html')