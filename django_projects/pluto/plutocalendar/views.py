from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CalendarUser, CalendarEvent, CalendarAuthToken
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from uuid import uuid4
# Create your views here.

def index(request):
    """View function for homep age of site."""

   
    #num_visits = request.session.get('num_visits', 0)
    #request.session['num_visits'] = num_visits + 1
    """
    context = {
        
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
        
    }
    """
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html') #context=context

def login(request):
    return render(request, 'plutocalendar/login.html')

def login_error(request, error_message, username):
    context = {
        "error_message" : error_message,
        "username" : username,
    }
    return render(request, 'plutocalendar/login.html', context=context)

def login_handler(request):
    if request.method != "POST":
        return login_error(request, "Expected HTTP POST", "")
    
    data = request.POST
    username = data.get("username")
    password = data.get("password")
    if username == "" or password != "123":
        return login_error(request, "Username and/or password incorrect", username)
    
    response = redirect(reverse('calendar'))
    response.set_cookie("username", username)
    response.set_cookie("auth_token", uuid4())
    return response

def calendar(request):
    username = request.COOKIES.get("username") 
    auth_token = request.COOKIES.get("auth_token")
    if username is None or auth_token is None:
        return login_error(request, "Please log in :)", "") 
    
    return render(request, 'plutocalendar/calendar.html')