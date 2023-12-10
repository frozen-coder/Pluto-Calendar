from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from datetime import datetime
# Create your models here.




class CalendarUser(models.Model):
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(default = "placeholder@placeholder.com",max_length=254, unique=True)
    #TODO: make sure to encrypt before launch
    password = models.CharField(max_length = 250)

class CalendarAuthToken(models.Model):
    uuid = models.CharField(max_length = 100, unique=True)
    user_id = models.ForeignKey(CalendarUser, on_delete=models.CASCADE)
    last_login = models.DateTimeField(auto_now = True)
    
    



class CustomUser(AbstractUser):
    pass
class CalendarEvent(models.Model):
    """
    Fields ;):):
    date
    summary 
    """
    title = models.CharField(max_length=35, help_text='Title of event')
    summary = models.CharField(max_length=250, help_text='Summary of event', blank=True)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    user_id = models.ForeignKey(CalendarUser, on_delete=models.CASCADE)