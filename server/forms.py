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
        exclude = []
        widgets = {'items': CheckboxSelectMultiple()}

    def __init__(self, *args, **kwargs):
        initial_first_name = kwargs.pop('server')

        super(CreateOrderForm, self).__init__(*args, **kwargs)

        self.fields['server'].initial = initial_first_name


OrderFormSet = formset_factory(CreateOrderForm, extra=3, max_num=6)
