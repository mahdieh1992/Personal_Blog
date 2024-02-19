from typing import Any
from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    ConfirmPassword=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'ConfirmPassword'
    }))
    class Meta:
        model=CustomUser
        fields=('email','password','ConfirmPassword')

        widgets={
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
            "password": forms.PasswordInput(
                attrs={"class": "form-control", "placeholder": "Password"}
            ),
   
        }
    def clean(self):
        password1=self.cleaned_data["password"]
        ConfirmPassword1=self.cleaned_data["ConfirmPassword"]
        if password1 != ConfirmPassword1:
            raise ValidationError('Password and ConfirmPassword does not match',code='does_not_match_password')
        

class LoginForm(forms.Form):
    email=forms.CharField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Enter Your Email'
    }))

    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Enter Your password'
    }))


        



