from django.db import models
from django import forms
from django.contrib.auth.forms import AuthenticationForm
# Create your models here.

class Client(models.Model):
    filled_at=models.DateTimeField(auto_now_add=True)
    client_name = models.CharField(max_length=50)
    client_email = models.CharField(max_length=100)
    client_message = models.TextField()


    def __str__(self):
        return self.client_name



