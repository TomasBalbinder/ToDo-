

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .utility import authentication
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm, CustomRegisterForm
from verify_email.email_handler import send_verification_email
from .models import TodoModel
from django.urls import reverse




# Create your views here



def home_page(request):
    return render(request, 'ToDoApp/home_page.html')



def sign_up_user(request):

    if request.method == "GET":
        return render(request, 'ToDoApp/signup_user.html', {'form' : CustomRegisterForm()}) #create form

    else:
        if  authentication.password(request) and authentication.nickname(request):
            messages.error(request, 'Nickname is Exist', extra_tags='nickname')
            messages.error(request, 'password is wrong', extra_tags='password')
                           
        elif authentication.password(request):
            messages.error(request, 'password is wrong.', extra_tags='password')                       
               
        elif authentication.nickname(request):
            messages.error(request, 'Nickname is Exist.', extra_tags='nickname')
                 
        else:               
            form = CustomRegisterForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                form.save()                
                messages.success(request, f"Account was created {username}", extra_tags='registration_sucess')
                form = UserCreationForm()
                return redirect('loginuser')
            else:
                form = CustomRegisterForm()
                return render(request, 'ToDoApp/signup_user.html', {'form' : form})

    return render(request, 'ToDoApp/signup_user.html', {'form' : CustomRegisterForm()})



def current_login(request):    
    return render(request, 'ToDoApp/current_login.html')




def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')



def login_user(request):

    if request.method == "GET":
        return render(request, 'ToDoApp/login_user.html', {'form' : UserCreationForm()})

    username = request.POST['username']
    password = request.POST['password1']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('current')
   
    else:
        messages.error(request, 'Wrong password or nickname.', extra_tags='nickname')        
    return render(request, 'ToDoApp/login_user.html', {'form' : UserCreationForm()})



def create_article(request):

    if request.method == "GET":
        form = TodoForm()
        return render(request, 'ToDoApp/create_article.html', {'form' : form})

    else:
        form = TodoForm(request.POST)
        newtodo = form.save(commit=False)
        newtodo.user = request.user
        newtodo.save()
        messages.add_message(request, messages.SUCCESS, f'TODO {newtodo.title} byl přidán na váš list')
        return redirect('current')



def show_posts(request):

    mydata = TodoModel.objects.filter(user=request.user)

    if not mydata:
        messages.error(request, 'Nemáte žadné příspěvky', extra_tags='noposts') 
        return render(request, 'ToDoApp/show_posts.html', {'mydata' : mydata})

    else:
        if request.method == "POST":
            id_list = request.POST.getlist('boxes')

            if not id_list:
                return render(request, 'ToDoApp/show_posts.html', {'mydata' : mydata})

            else:                  
                mydata.filter(pk__in=id_list).delete()
                messages.success(request, ("Delete data was success!"))
                return redirect('current')

        else:		
            return render(request, 'ToDoApp/show_posts.html', {'mydata' : mydata})
			








            