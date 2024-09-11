from django.db.models import Count, Q
from django.shortcuts import render
from django.views import View
from core.models import Appointment
from core.forms import AppointmentFilterForm

class ReportCountView(View):
    """
    View for generating appointment reports based on filters.
    """

    template_name = 'core/reporting/report.html'

    def get(self, request):
        """
        Handle GET request for generating the report form.
        """
        form = AppointmentFilterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Handle POST request for generating the report based on form data.
        """
        form = AppointmentFilterForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            doctor_name = form.cleaned_data['doctor_name']
            status = form.cleaned_data['status']

            # Filter appointments by date range
            if start_date and end_date:
                appointments = Appointment.objects.filter(scheduled_at__date__range=[start_date, end_date])
            elif start_date:
                appointments = Appointment.objects.filter(scheduled_at__date__gte=start_date)
            elif end_date:
                appointments = Appointment.objects.filter(scheduled_at__date__lte=end_date)
            else:
                appointments = Appointment.objects.all()
            # Filter by doctor name if provided
            if doctor_name:
                appointments = appointments.filter(
                    Q(doctor__user__first_name__icontains=doctor_name) |
                    Q(doctor__user__last_name__icontains=doctor_name)
                )

            # Filter by status
            if status == 'completed':
                appointments = appointments.filter(is_completed=True)
            elif status == 'pending':
                appointments = appointments.filter(is_completed=False)

            # Annotate appointment counts
            appointment_counts = appointments.values('scheduled_at__date').annotate(
                count=Count('id'),
                completed_count=Count('id', filter=Q(is_completed=True)),
                pending_count=Count('id', filter=Q(is_completed=False))
            )

            return render(request, self.template_name, {
                'appointments': appointments,
                'appointment_counts': appointment_counts,
                'form': form
            })
        return render(request, self.template_name, {'form': form})


class ReportDetailView(View):
    """
    View for displaying detailed report for a specific date.
    """

    template_name = 'core/reporting/report_detail.html'

    def get(self, request, date):
        """
        Handle GET request for displaying the detailed report for a specific date.
        """
        form = AppointmentFilterForm(request.GET, disable_fields=['start_date', 'end_date'])
        appointments = Appointment.objects.filter(scheduled_at__date=date)

        # Apply filters from query parameters
        if form.is_valid():
            doctor_name = form.cleaned_data['doctor_name']
            status = form.cleaned_data['status']

            if doctor_name:
                appointments = appointments.filter(
                    Q(doctor__user__first_name__icontains=doctor_name) |
                    Q(doctor__user__last_name__icontains=doctor_name)
                )

            # Filter by status
            if status == 'completed':
                appointments = appointments.filter(is_completed=True)
            elif status == 'pending':
                appointments = appointments.filter(is_completed=False)

        return render(request, self.template_name, {
            'appointments': appointments,
            'date': date,
            'form': form
        })
