from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name = 'login'),
    path('login_handler/', views.login_handler, name = 'login_handler'),
    path('calendar/', views.calendar, name = 'calendar'),
    path('create_user/', views.create_user , name = 'create_user'),
    path('create_user_handler', views.create_user_handler, name = 'create_user_handler'),
    path('create_user_confirmed', views.create_user_confirmed, name = 'create_user_confirmed'),
    path('logout/', views.logout_user, name = 'logout'),
    path('create_task/', views.create_task, name ='create_task'),
    path('create_task_handler', views.create_task_handler, name = 'create_task_handler')
]