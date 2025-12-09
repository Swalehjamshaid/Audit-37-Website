from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class AuditForm(forms.Form):
    url = forms.URLField(label="Enter Railway Website URL", widget=forms.URLInput(attrs={'placeholder': 'https://www.indianrailways.gov.in'}))
