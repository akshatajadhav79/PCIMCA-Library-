from django.core import validators
from django import forms
from .models import post

class StudentRegistration(forms.ModelForm):
    class Meta:
        model = post
        fields = ['title', 'email','password']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(render_value=True, attrs={'class':'form-control'}),
        }