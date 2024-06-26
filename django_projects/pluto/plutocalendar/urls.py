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
    path('create_task_handler', views.create_task_handler, name = 'create_task_handler'),
    path('delete_task_handler', views.delete_task_handler, name = 'delete_task_handler'),
    path('create_task_test', views.create_task_test, name = 'create_task_test'),
    path('delete_task_test', views.delete_task_test, name = 'delete_task_test'),
    path('get_tasks_test', views.get_tasks_test, name = 'get_task_test'),
    path('get_tasks_date_range', views.get_tasks_date_range, name = 'get_tasks_date_range'),
    path('delete_user', views.delete_user, name = 'delete_user'),
    path('delete_user_confirmed', views.delete_user_confirmed, name = 'delete_user_confirmed'),
    path('delete_user_handler', views.delete_user_handler, name='delete_user_handler'),
]