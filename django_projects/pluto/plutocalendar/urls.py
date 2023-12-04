from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name = 'login'),
    path('login_handler/', views.login_handler, name = 'login_handler'),
    path('calendar/', views.calendar, name = 'calendar')
]