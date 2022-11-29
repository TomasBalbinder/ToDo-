

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .utility import authentication
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm, CustomRegisterForm
from .models import TodoModel
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

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
            if request.method == "POST":               
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




def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "ToDoApp/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="ToDoApp/password/password_reset.html", context={"password_reset_form":password_reset_form})
