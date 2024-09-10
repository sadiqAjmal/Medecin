from django import forms
from .models import Doctor, Patient
from users.models import User

class DoctorForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), required=False)
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance.pk:  
            if User.objects.filter(username=username).exclude(id=self.instance.user.id).exists():
                raise forms.ValidationError("This username is already in use.")
        else:  
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("This username is already in use.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance.pk: 
            if User.objects.filter(email=email).exclude(id=self.instance.user.id).exists():
                raise forms.ValidationError("This email is already in use.")
        else:  
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("This email is already in use.")
        return email
    
    class Meta:
        model = Doctor
        fields = ['specialization']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['username'].initial = instance.user.username
            self.fields['email'].initial = instance.user.email
            self.fields['phone_number'].initial = instance.user.phone_number
            self.fields['password'].required = False
        
class PatientForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), required=False)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance.pk:  
            if User.objects.filter(username=username).exclude(id=self.instance.user.id).exists():
                raise forms.ValidationError("This username is already in use.")
        else:  
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("This username is already in use.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance.pk: 
            if User.objects.filter(email=email).exclude(id=self.instance.user.id).exists():
                raise forms.ValidationError("This email is already in use.")
        else:  
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("This email is already in use.")
        return email

    class Meta:
        model = Patient
        fields = ['date_of_birth', 'gender']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        
        if instance and instance.user:
            self.fields['username'].initial = instance.user.username
            self.fields['email'].initial = instance.user.email
            self.fields['phone_number'].initial = instance.user.phone_number
            self.fields['password'].required = False



