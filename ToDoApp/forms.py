from xml.dom import ValidationErr
from django import forms
from .models import TodoModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TodoForm(forms.ModelForm):
    class Meta:
        model = TodoModel
        fields = ['title', 'memo', 'important']


class CustomRegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', min_length=5, max_length=30)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', max_length=200, help_text="Required")

