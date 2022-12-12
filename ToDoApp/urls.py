from django.urls import path
from ToDoApp import views

app_name = "ToDoApp"   


urlpatterns = [
   
    path("password_reset/", views.password_reset_request, name="password_reset")
]