from django.contrib.auth.forms import UserCreationForm
from django import forms
from server.models import MenuItem

# class NewUserCreation(UserCreationForm):
#     first_name = forms.CharField()
#     restaurant_name = forms.CharField()
#     number_of_tables = forms.IntegerField()


class ServerCreateForm(UserCreationForm):
    name = forms.CharField()


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ('name', 'description', 'price', 'item_type', 'photo')
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Name'}),
                   'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Item Description'}),
                   'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
                   'item_type': forms.Select(attrs={'class': 'form-control'}),
                   'photo': forms.ClearableFileInput(attrs={'type': 'file'})
                   }
        labels = {'name': '', 'description': '', 'price': '', 'item_type': '', 'photo': 'Add Photo'}
