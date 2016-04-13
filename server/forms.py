from django.contrib.auth.forms import UserCreationForm
from django import forms
from server.models import OrderedItem
from django.forms.widgets import RadioSelect
from django.forms import formset_factory


# class NewUserCreation(UserCreationForm):
#     first_name = forms.CharField()
#     restaurant_name = forms.CharField()
#     number_of_tables = forms.IntegerField()
#

class ServerCreateForm(UserCreationForm):
    name = forms.CharField()



#
# this may be completely unnecessary
# class OrderBaseFormSet(forms.BaseInlineFormSet):
#     def clean(self):
#         if any(self.errors):
#             return
#         counter = 1
#         for form in self.forms:
#             form.cleaned_data['seat_number'] = counter
#             counter += 1
#         return form.cleaned_data
#


#
