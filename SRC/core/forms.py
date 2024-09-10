from django import forms
from .models import Doctor
from users.models import User

class DoctorForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), required=False)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists() and not self.instance.user.email == email:
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
        
