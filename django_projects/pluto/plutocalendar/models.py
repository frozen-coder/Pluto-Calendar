from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from datetime import date
# Create your models here.




class CalendarUser(models.Model):
    username = models.CharField(max_length=25, unique=True)
    
    #TODO: make sure to encrypt before launch
    password = models.CharField(max_length = 250)

class CalendarAuthToken(models.Model):
    uuid = models.CharField(max_length = 100, unique=True)
    user_id = models.ForeignKey(CalendarUser, on_delete=models.CASCADE)
    last_login = models.DateTimeField(auto_now = True)
    """
    @property
    def is_expired(self):
        Determines if the book is overdue based on due date and current date.
        return bool(self.logi and date.today() > self.due_back)
    """


class CustomUser(AbstractUser):
    pass
class CalendarEvent(models.Model):
    """
    Fields ;):):
    date
    summary 
    """
    summary = models.CharField(max_length=250, help_text='Summary of event')
    date = models.DateField(auto_now=False, auto_now_add=False)
    user_id = models.ForeignKey(CalendarUser, on_delete=models.CASCADE)