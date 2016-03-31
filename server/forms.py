from django.contrib.auth.forms import UserCreationForm
from django import forms
# from theonsapp.models import City


class NewUserCreation(UserCreationForm):
    first_name = forms.CharField()
    restaurant_name = forms.CharField()

    # class Meta:
    #     fields = ['username', 'password', 'name']
