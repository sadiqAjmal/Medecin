from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from core.models import Patient
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.views import View
from core.forms import PatientForm
from django.views.generic.edit import FormView,UpdateView,DeleteView,CreateView
from django.core.exceptions import ValidationError
from django.db import transaction
 
User = get_user_model()
 
class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'core/patients/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 5
    def get_queryset(self):
        if self.request.user.is_doctor:
            return Patient.objects.filter(appointment__doctor=self.request.user.doctor)
        return Patient.objects.all()
   
    login_url = '/login/'
 
class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'core/patients/patient_details.html'
    context_object_name = 'patient'
   
    login_url = '/login/'
 
class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'core/patients/patient_form.html'
    success_url = reverse_lazy('patient_list')
 
    def form_valid(self, form):
        try:
            user = User.objects.create(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number']
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            form.instance.user = user
            return super().form_valid(form)
        except Exception as e:
            form.add_error(None, "An error occurred while creating the user. Please try again.")
            return self.form_invalid(form)
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Patient'
        context['button_name'] = 'Create'
        return context
 
 
class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'core/patients/patient_form.html'
    success_url = reverse_lazy('patient_list')
 
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
        context['title'] = 'Update Patient'
        context['button_name'] = 'Update'
        return context
 
class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'core/patients/patient_confirm_delete.html'
    success_url = reverse_lazy('patient_list')
 
 