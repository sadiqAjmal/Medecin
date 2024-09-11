from django import forms
from .models import Doctor, Patient
from users.models import User
from django import forms
class DoctorForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), required=False)

    class Meta:
        model = Doctor
        fields = ['specialization']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # For a new Doctor, current_user_pk will be None, so we don't exclude any users
            current_user_pk = None
            if self.instance and self.instance.pk:
                # For an existing Doctor, exclude the current user from the check
                user = getattr(self.instance, 'user', None)
                if user:
                    current_user_pk = user.pk
            
            # Check if another user with this username exists, excluding the current user if available
            if User.objects.filter(username=username).exclude(pk=current_user_pk).exists():
                raise forms.ValidationError("This username is already in use.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # For a new Doctor, current_user_pk will be None, so we don't exclude any users
            current_user_pk = None
            if self.instance and self.instance.pk:
                # For an existing Doctor, exclude the current user from the check
                user = getattr(self.instance, 'user', None)
                if user:
                    current_user_pk = user.pk
            
            # Check if another user with this email exists, excluding the current user if available
            if User.objects.filter(email=email).exclude(pk=current_user_pk).exists():
                raise forms.ValidationError("This email is already in use.")
        return email
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.user:
            # Initialize fields with user data if available
            self.fields['first_name'].initial = instance.user.first_name
            self.fields['last_name'].initial = instance.user.last_name
            self.fields['username'].initial = instance.user.username
            self.fields['email'].initial = instance.user.email
            self.fields['phone_number'].initial = instance.user.phone_number
            self.fields['password'].required = False


class PatientForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), required=False)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Patient
        fields = ['date_of_birth', 'gender']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Get the current user instance if available
            current_user_pk = None
            if self.instance and self.instance.pk:
                user = getattr(self.instance, 'user', None)
                if user:
                    current_user_pk = user.pk
            
            # Check if another user with this username exists, excluding the current user if available
            if User.objects.filter(username=username).exclude(pk=current_user_pk).exists():
                raise forms.ValidationError("This username is already in use.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Get the current user instance if available
            current_user_pk = None
            if self.instance and self.instance.pk:
                user = getattr(self.instance, 'user', None)
                if user:
                    current_user_pk = user.pk
            
            # Check if another user with this email exists, excluding the current user if available
            if User.objects.filter(email=email).exclude(pk=current_user_pk).exists():
                raise forms.ValidationError("This email is already in use.")
        return email

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        
        if instance and instance.user:
            # Initialize fields with user data if available
            self.fields['first_name'].initial = instance.user.first_name
            self.fields['last_name'].initial = instance.user.last_name
            self.fields['username'].initial = instance.user.username
            self.fields['email'].initial = instance.user.email
            self.fields['phone_number'].initial = instance.user.phone_number
            self.fields['password'].required = False

class AppointmentFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('', 'All'),         # Empty string for "All"
        ('pending', 'Pending'),
        ('completed', 'Completed')
    ]

    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    doctor_name = forms.CharField(max_length=50, required=False)
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label='Status')

    def __init__(self, *args, **kwargs):
        disable_fields = kwargs.pop('disable_fields', [])
        super().__init__(*args, **kwargs)

        # Apply necessary styling to fields
        self.fields['start_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['end_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['doctor_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})

        # Disable fields if needed
        for field in disable_fields:
            if field in self.fields:
                self.fields[field].disabled = True