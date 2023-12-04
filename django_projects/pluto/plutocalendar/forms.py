import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


from django import forms


class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)
