from django.db import models
from django import forms
from django.contrib.auth.forms import AuthenticationForm
# Create your models here.

# messages db

class Client(models.Model):
    filled_at=models.DateTimeField(auto_now_add=True)
    client_name = models.CharField(max_length=50)
    client_email = models.CharField(max_length=100)
    client_message = models.TextField()


    def __str__(self):
        return self.client_name


# drawings db

class Drawing(models.Model):
    drawing_name=models.CharField(max_length=100)
    drawing_artist=models.CharField(max_length=50)
    drawing_price=models.IntegerField()
    drawing_img=models.ImageField(upload_to = "drawings/")


    def __str__(self):
        return self.drawing_name


# register db

class User1(models.Model):
    user_name=models.CharField(max_length=50)
    user_email=models.CharField(max_length=100)
    user_password1=models.CharField(max_length=100)
    user_password2=models.CharField(max_length=100)

    def __str__(self):
        return self.user_name

