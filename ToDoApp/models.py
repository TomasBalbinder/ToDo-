from django.db import models
from django.contrib.auth.models import User
from random import choice
from PIL import Image

# Create your models here.

class TodoModel(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
   

    def __str__(self):
        return str(self.user.id) + " " + self.user.username + " " + self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default=choice(['default1.jpg', 'default2.jpg']), upload_to='profile_pics')

    def __str__(self):
        return f' {self.user.username} Profile'


    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 100 or img.width > 100:
            output_size = (200,200)
            img.thumbnail(output_size)
            img.save(self.image.path)
