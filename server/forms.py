from django.contrib.auth.forms import UserCreationForm
from django import forms
from server.models import Order
from django.forms.widgets import CheckboxSelectMultiple
from django.forms import formset_factory


class NewUserCreation(UserCreationForm):
    first_name = forms.CharField()
    restaurant_name = forms.CharField()


class ServerCreateForm(UserCreationForm):
    name = forms.CharField()


class CreateOrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['items']
        widgets = {'items': CheckboxSelectMultiple()}

order_form_set = formset_factory(CreateOrderForm, extra=2)
