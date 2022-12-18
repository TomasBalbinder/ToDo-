from django.contrib import admin
from .models import TodoModel, Profile
# Register your models here.





class ToDoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(TodoModel, ToDoAdmin)
admin.site.register(Profile)