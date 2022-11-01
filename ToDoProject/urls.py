"""ToDoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from ToDoApp import views


urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home'),
    path('current/', views.current_login, name='current'),

    # authentication
    path('signup/', views.sign_up_user, name='signupuser'),    
    path('logout/', views.logout_user, name='logoutuser'),
    path('login/', views.login_user, name='loginuser'),

    # work with todo
    path('create/', views.create_article, name='createtodo'),
    path('posts/', views.show_posts, name='showposts'),

    # verification from email register 
    path('verification/', include('verify_email.urls')),

]