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

class DoctorDashboardView(LoginRequiredMixin,TemplateView):
    template_name='core/doctors/doctor_dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patients'] = Patient.objects.filter(appointment__doctor=self.request.user.doctor)
        context['appointments'] = Appointment.objects.filter(doctor=self.request.user.doctor)
        context['doctor'] = Doctor.objects.get(user=self.request.user)
        return context
    
class DoctorListView(LoginRequiredMixin, ListView):
    model = Doctor
    template_name = 'core/doctors/doctors_list.html'
    context_object_name = 'doctors'
    
    def get_queryset(self):
        query = self.request.GET.get('search_query', '')
        specialization_filter = self.request.GET.get('filter_specialization', '')
        doctors = Doctor.objects.all()
        if query:
            doctors = doctors.filter(
                Q(user__username__icontains=query) |
                Q(user__phone_number__icontains=query) |
                Q(user__email__icontains=query)
            )
        if specialization_filter:
            doctors = doctors.filter(specialization__icontains=specialization_filter)
        return doctors
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search_query', '')
        context['specialization_filter'] = self.request.GET.get('filter_specialization', '')
        context['specializations'] = Doctor.objects.values_list('specialization', flat=True).distinct()
        return context

class DoctorDetailView(LoginRequiredMixin, DetailView):
    model = Doctor
    template_name = 'core/doctors/doctor_details.html'
    context_object_name = 'doctor'


User = get_user_model()


class DoctorCreateView(AdminRequiredMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'core/doctors/doctor_form.html'
    success_url = reverse_lazy('doctor_list')
    
    def form_valid(self, form):
        user = User.objects.create(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            phone_number=form.cleaned_data['phone_number']
        )
        user.set_password(form.cleaned_data['password'])
        user.is_doctor = True
        user.save()
        form.instance.user = user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Doctor'
        context['button_name'] = 'Create'
        return context


class DoctorUpdateView(AdminRequiredMixin, UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'core/doctors/doctor_form.html'
    success_url = reverse_lazy('doctor_list')
    
    def form_valid(self, form):
        user = form.instance.user
        user.username = form.cleaned_data['username']
        user.email = form.cleaned_data['email']
        user.phone_number = form.cleaned_data['phone_number']
        if form.cleaned_data['password']:
            user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Doctor'
        context['button_name'] = 'Update'
        return context


class DoctorDeleteView(AdminRequiredMixin,DeleteView):
    model = Doctor
    template_name = 'core/doctors/doctor_confirm_delete.html'
    success_url = reverse_lazy('doctor_list')
