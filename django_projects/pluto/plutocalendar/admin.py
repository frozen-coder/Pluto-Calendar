from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CalendarUser, CalendarAuthToken, CalendarEvent
#register models here
admin.site.register(CustomUser, UserAdmin)
admin.site.register(CalendarUser)
admin.site.register(CalendarAuthToken)
admin.site.register(CalendarEvent)