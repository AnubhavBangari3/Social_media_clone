#Profiles
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from .models import Profile
from django import forms

class ProfileModelForm(ModelForm):
    class Meta:
        model=Profile
        fields=('first_name','last_name','bio','avatar',)

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=120, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=120, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )