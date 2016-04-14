from django.contrib.auth.forms import UserCreationForm
from django import forms
from server.models import MenuItem, Menu
# class NewUserCreation(UserCreationForm):
#     first_name = forms.CharField()
#     restaurant_name = forms.CharField()
#     number_of_tables = forms.IntegerField()


class EmployeeCreateForm(UserCreationForm):
    name = forms.CharField()

    class Meta:
        fields = ['username', 'password1', 'password2']


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ('name', 'description', 'price', 'item_type', 'photo')
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Name'}),
                   'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Item Description', 'rows': '4'}),
                   'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
                   'item_type': forms.Select(attrs={'class': 'form-control'}),
                   'photo': forms.ClearableFileInput(attrs={'type': 'file'})
                   }
        labels = {'name': '', 'description': '', 'price': '', 'item_type': '', 'photo': 'Add Photo'}


class MenuCreateForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'item']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Menu Name'}),
                   'item': forms.CheckboxSelectMultiple(attrs={'class': 'checkboxinline'})
                   }
        labels = {'name': '', 'item': 'Menu Items To Include'}
