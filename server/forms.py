from django.contrib.auth.forms import UserCreationForm
from django import forms
# from theonsapp.models import City


class NewUserCreation(UserCreationForm):
    name = forms.CharField()

    # class Meta:
    #     fields = ['username', 'password', 'name']
