from django.contrib import admin
from .models import TodoModel
# Register your models here.





class ToDoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)



admin.site.register(TodoModel, ToDoAdmin)