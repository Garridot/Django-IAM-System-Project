from django_registration.forms import RegistrationForm
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm
from models.models import *
from django import forms



class CustomRegistrationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = CustomUser
        
class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))

class CustomPasswordResetForm(PasswordResetForm):
    # Ensure that the 'email' field is defined
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Please enter a valid email address.')

        # Your additional checks for invalid or not found email
        # For example, check if the email exists in your user database
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Email address not found.')

        return email