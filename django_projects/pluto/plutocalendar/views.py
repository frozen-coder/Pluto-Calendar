from django.shortcuts import render, redirect
from .models import CalendarUser, CalendarEvent, CalendarAuthToken
from django.shortcuts import redirect
from django.urls import reverse
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from django.contrib.auth import logout
from time import mktime
from django.http import JsonResponse

# Create your views here.

def index(request):
    """View function for homepage of site."""
    context = {}
    context = add_user_to_context(request, context)
    print(request.COOKIES.get("auth_token"))
    print(is_logged_in(request))
    print(context)
    return render(request, 'index.html', context = context) 

def login(request):
    if(is_logged_in(request)):
        return redirect(reverse('index'))
    context = {}
    context = add_user_to_context(request, context)
    return render(request, 'plutocalendar/login.html')

def login_error(request, error_message, username):
    
    context = {
        "error_message" : error_message,
        "form_username" : username,
    }
    context = add_user_to_context(request, context)
    return render(request, 'plutocalendar/login.html', context=context)

def login_handler(request):

    if request.method != "POST":
        return login_error(request, "Expected HTTP POST", "")
    if(is_logged_in(request)):
        return redirect(reverse('index'))
    data = request.POST
    username = data.get("username")
    password = data.get("password")
    print(username)
    print(password)
    #TODO: clean data
    if username == None or username == "" or password == None or password == "":
        return login_error(request, "Username and/or password incorect", username)
    
    user_query_set = CalendarUser.objects.filter(username__exact=username)
    if not user_query_set:
        return login_error(request, "User not found", username)
    
    user = user_query_set.get()
    #print(user)
    if user.password != password:
        return login_error(request, "Password incorect", username)
    
    auth_token = get_or_create_auth_token(user)

    response = redirect(reverse('calendar'))
    response.set_cookie("username", username)
    response.set_cookie("auth_token", auth_token)
    return response

def logout_user(request):
    if(not is_logged_in(request)):
        return redirect(reverse('index'))
    
    response = redirect(reverse('index'))
    delete_auth_token_request(request)
    response.delete_cookie("username")
    response.delete_cookie("auth_token")
    return response


def create_user_error(request, informationTuple):
    context = {
        "error_message" : informationTuple[0],
        "form_username": informationTuple[1],
        "email": informationTuple[2],
        "username": request.COOKIES.get("username"),
    }
    context = add_user_to_context(request, context)
    return render(request, 'plutocalendar/create_user.html', context = context)

def create_user_handler(request):
    if request.method != "POST":
        informationTuple = ("Expected HTTP POST","","")
        return create_user_error(request, informationTuple)

    data = request.POST
    #TODO: Clean the data before making a new user
    potential_username = data.get("username")
    potential_password_one = data.get("password")
    potential_password_two = data.get("password_repeat")
    email = data.get("email")
    if(potential_username is None or potential_password_one is None or potential_password_two is None or email is None):
        informationTuple = ("Please fill in the entire form", potential_username, email)
        return create_user_error(request, informationTuple)
    
    if(CalendarUser.objects.filter(username__exact=potential_username)):
        informationTuple = ("Username already in use", potential_username, email)
        return create_user_error(request, informationTuple)
    if(CalendarUser.objects.filter(email__exact=email)):
        informationTuple = ("Email already in use", potential_username, email)
        return create_user_error(request, informationTuple)
    if(potential_password_one != potential_password_two):
        return create_user_error(request, ("Passwords do not match", potential_username))
    user = CalendarUser()
    user.email = email
    user.username = potential_username
    user.password = potential_password_one
    user.save()
    return redirect(reverse('create_user_confirmed'))

def create_user(request):
    context = {}
    context = add_user_to_context(request, context)
    return render(request, "plutocalendar/create_user.html", context=context)

def create_user_confirmed(request):
    context = {}
    context = add_user_to_context(request, context)
    return render(request, "plutocalendar/create_user_confirmed.html",context=context)

def delete_user_error(request, informationTuple):
    context = {
        "error_message" : informationTuple[0],
        "username": request.COOKIES.get("username"),
    }
    context = add_user_to_context(request, context)
    return render(request, 'plutocalendar/create_user.html', context = context)

def delete_user_handler(request):
    if (is_logged_in(request)) == False:
        return login_error(request, "Please log in :)", request.COOKIES.get("username") ) 
    if request.method != "POST":
        informationTuple = ("Expected HTTP POST","","")
        return create_user_error(request, informationTuple)

    data = request.POST
    #TODO: Clean the data before deleting user and also encrypt passwords
    password_one = data.get("password")
    password_two = data.get("password_repeat")
   
    if(password_one is None or password_two is None):
        informationTuple = ("Passwords Must Match")
        return create_user_error(request, informationTuple)
    
     
    if(password_one != password_two):
        return create_user_error(request, ("Passwords do not match"))
    user = CalendarUser.objects.filter(username__exact=request.COOKIES.get("username")).get()
    if(user.password != password_one):
        informationTuple = ("Password is incorrect")
        return create_user_error(request, informationTuple)
    user.delete()
    return delete_user_confirmed(request)

def delete_user(request):
    context = {}
    context = add_user_to_context(request, context)
    return render(request, "plutocalendar/delete_user.html", context=context)

def delete_user_confirmed(request):
    context = {}
    context = add_user_to_context(request, context)
    return render(request, "plutocalendar/delete_user_confirmed.html",context=context)


def calendar(request):
    
    if (is_logged_in(request)) == False:
        return login_error(request, "Please log in :)", request.COOKIES.get("username") ) 
    context = {}
    context = add_user_to_context(request, context)
    
    return render(request, 'plutocalendar/calendar.html', context=context)

def is_logged_in(request):
    username = request.COOKIES.get("username") 
    auth_token = request.COOKIES.get("auth_token")
    if(username is None or auth_token is None):
        return False

    user_query_set = CalendarUser.objects.filter(username__exact=username)
    if(not user_query_set):
        return False

    user = user_query_set.get()
    auth_token_query_set = CalendarAuthToken.objects.filter(user_id__exact=user.pk)
    if(not auth_token_query_set):
        return False

    auth_token = auth_token_query_set.get()
    if(is_auth_token_expired(auth_token)):
        delete_auth_token(auth_token)
        return False

    update_auth_token(auth_token)
    return True

def create_task_handler(request):
    if request.method != "POST":
        #Expected HTTP POST
        return JsonResponse({"success", "false"})
    data = request.POST
    date = data.get("date")
    title = data.get("title")
    start_time = data.get("eventTimeFrom")
    end_time = data.get("eventTimeTo")
    event = CalendarEvent()
    if(date == None or start_time == None or end_time == None or title == None):
        return JsonResponse({"success", "false"})
    start_time_array = start_time.split(":")
    start_time_hour = int(start_time_array[0])
    if(start_time_array[1].split(" ")[1] == "PM"):
        start_time_hour  = start_time_hour + 12
    start_time_minute = int(start_time_array[1].split(" ")[0])
    
    end_time_array = end_time.split(":")
    end_time_hour = int(end_time_array[0])
    if(end_time_array[1].split(" ")[1] == "PM"):
        end_time_hour  = end_time_hour + 12

    end_time_minute = int(end_time_array[1].split(" ")[0])
    #creating an instance of  
    # datetime.time 
    # time(hour = 0, minute = 0, second = 0) 
    event.start_time = datetime.time(start_time_hour, start_time_minute) 
    event.end_time = datetime.time(end_time_hour, end_time_minute) 
    date_array = date.split("-")

    #%Y-%m-%d',             # '2006-10-25'
    event.date= datetime.datetime(int(date_array[0]), int(date_array[1]), int(date_array[2]))
    event.save()
    return JsonResponse({"success", "true"})
  
    
def get_or_create_auth_token(user):
    auth_token_query_set = CalendarAuthToken.objects.filter(user_id__exact=user.pk)
    if auth_token_query_set:
        #TODO: implement time limit in model or here
        auth_token = auth_token_query_set.get()
    else:
        auth_token = CalendarAuthToken()
        auth_token.user_id = user
        auth_token.uuid = uuid4()
    
    update_auth_token(auth_token)
    return auth_token.uuid

def delete_auth_token(authtoken):
    authtoken.delete()
    return

def delete_auth_token_request(request):
    auth_token_uuid4 = request.COOKIES.get("auth_token")
    delete_auth_token(CalendarAuthToken.objects.filter(uuid__exact=auth_token_uuid4).get())
    return

def update_auth_token(authtoken):
    authtoken.date = datetime.now(timezone.utc)
    authtoken.save()
    return

def is_auth_token_expired(authtoken):
        NUMBER_OF_SECONDS = 86400 # seconds in 24 hours
        curr_date = datetime.now(timezone.utc)
        return bool(curr_date > (timedelta(seconds=NUMBER_OF_SECONDS) + authtoken.last_login))

def add_user_to_context(request, context):
    if(is_logged_in(request)):
        return context | {"username": request.COOKIES.get("username")}
    return context
