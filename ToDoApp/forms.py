
from django import forms
from .models import TodoModel, User
from django.contrib.auth.forms import UserCreationForm


class TodoForm(forms.ModelForm):
    class Meta:
        model = TodoModel
        fields = ['title', 'memo', 'important']



class CustomRegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', min_length=2, max_length=30)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', max_length=200)
    
    class Meta:
        model = User
        fields = ['username','password1','password2','email']




class ResetForm(forms.ModelForm):

    email = forms.EmailField(label='Email', max_length=200)
    
    class Meta:
        model = User
        fields = ['email']  