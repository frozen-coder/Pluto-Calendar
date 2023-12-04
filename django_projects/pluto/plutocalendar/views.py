from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CalendarUser, CalendarEvent, CalendarAuthToken
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from uuid import uuid4
from datetime import datetime


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
    if username == None or username == "" or password == None or password == "":
        return login_error(request, "Username and/or password incorect", username)
    
    user_query_set = CalendarUser.objects.filter(username__exact=username)
    if not user_query_set:
        return login_error(request, "User not found", username)
    
    user = user_query_set.get()
    print(user)
    if user.password != password:
        return login_error(request, "Password incorect", username)
    
    auth_token = get_or_create_auth_token(user)

    response = redirect(reverse('calendar'))
    response.set_cookie("username", username)
    response.set_cookie("auth_token", auth_token)
    return response

def create_user_error(request, informationTuple):
    context = {
        "error_message" : informationTuple[0],
        "username": informationTuple[1],
        "password_one": informationTuple[2],
        "password_two": informationTuple[3],
    }
    return render(request, 'plutocalendar/create_user.html', context = context)

def create_user_handler(request):
    if request.method != "POST":
        informationTuple = ("Expected HTTP POST","","","")
        return create_user_error(request, informationTuple)

    data = request.POST
    potential_username = data.get("username")
    potential_password_one = data.get("password")
    potential_password_two = data.get("password_repeat")

    if(potential_username is None or potential_password_one is None or potential_password_two is None):
        informationTuple = ("Please fill in the entire form", potential_username)
        return create_user_error(request, informationTuple)
    
    if(CalendarUser.objects.filter(username__exact=potential_username)):
        return create_user_error(request, ("Username already in use", potential_username))
    if(potential_password_one != potential_password_two):
        return create_user_error(request, ("Passwords do not match", potential_username))
    user = CalendarUser()
    
    
    




    


def create_user(request):
    return render(request, "plutocalendar/create_user.html")


def calendar(request):
    username = request.COOKIES.get("username") 
    auth_token = request.COOKIES.get("auth_token")
    if (is_logged_in(username, auth_token)) == False:
        return login_error(request, "Please log in :)", "") 
    
    
    return render(request, 'plutocalendar/calendar.html')

def is_logged_in(username, password):
    if(username is None or password is None):
        return False
    user_query_set = CalendarUser.objects.filter(username__exact=username)
    if(not user_query_set):
        return False
    user = user_query_set.get()
    auth_token_query_set = CalendarAuthToken.objects.filter(user_id__exact=user.pk)
    if(not auth_token_query_set):
        return False
    auth_token = auth_token_query_set.get()
    if(auth_token.is_expired):
        auth_token.delete()
        return False
    return True


def get_or_create_auth_token(user):
    auth_token_query_set = CalendarAuthToken.objects.filter(user_id__exact=user.pk)
    if auth_token_query_set:
        #TODO: implement time limit in model or here
        auth_token = auth_token_query_set.get()
    else:
        auth_token = CalendarAuthToken()
        auth_token.user_id = user
        auth_token.uuid = uuid4()
    
    auth_token.last_login = datetime.now()
    auth_token.save()
    return auth_token.uuid
        