from django.contrib.auth.forms import UserCreationForm
from django import forms
from server.models import Order, MenuItem
from django.forms.widgets import CheckboxSelectMultiple


class NewUserCreation(UserCreationForm):
    first_name = forms.CharField()
    restaurant_name = forms.CharField()


class ServerCreateForm(UserCreationForm):
    name = forms.CharField()


class CreateOrderForm(forms.ModelForm):
    class Meta:
        CHOICES = MenuItem.objects.all()
        model = Order
        fields = ['items']
        widgets = {'items': CheckboxSelectMultiple(choices=((item.id, item.name) for item in CHOICES))}
