import email
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .utility import authentication
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm, CustomRegisterForm
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token   




# Create your views here



def home(request):
    return render(request, 'ToDoApp/home.html')


def signupuser(request):

    if request.method == "GET":
        return render(request, 'ToDoApp/singupuser.html', {'form' : CustomRegisterForm()}) #create form

    else:
        if  authentication.password(request) and authentication.nickname(request):
            messages.error(request, 'Nickname is Exist', extra_tags='nickname')
            messages.error(request, 'password is wrong', extra_tags='password')
                           
        elif authentication.password(request):
            messages.error(request, 'password is wrong.', extra_tags='password')                       
               
        elif authentication.nickname(request):
            messages.error(request, 'Nickname is Exist.', extra_tags='nickname')
                 
        else:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'], email=request.POST['email']) #very important use method POST for URL encryption
            user.save()
            login(request, user)
            return redirect('current')

    return render(request, 'ToDoApp/singupuser.html', {'form' : CustomRegisterForm()})

def current(request):    
    return render(request, 'ToDoApp/currenttodo.html')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def loginuser(request):

    if request.method == "GET":
        return render(request, 'ToDoApp/loginuser.html', {'form' : UserCreationForm()})

    username = request.POST['username']
    password = request.POST['password1']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('current')
   
    else:
        messages.error(request, 'Wrong password or nickname.', extra_tags='nickname')        
    return render(request, 'ToDoApp/loginuser.html', {'form' : UserCreationForm()})



def createtodo(request):
    if request.method == "GET":
        form = TodoForm()
        return render(request, 'ToDoApp/createtodo.html', {'form' : form})
    else:
        form = TodoForm(request.POST)
        newtodo = form.save(commit=False)
        newtodo.user = request.user
        newtodo.save()
        return redirect('current')
















            