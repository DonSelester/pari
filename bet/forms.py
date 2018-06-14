from django import forms
from .models import *
from django.utils import timezone

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class PlayerForm(forms.ModelForm):
    birthday = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='День рождения')
    class Meta():
        model = Player
        fields = ( 'full_name', 'birthday', 'country', 'phone')

class OperationForm(forms.ModelForm):
    class Meta():
        model = Operation
        fields = ('account_number', 'date', 'card', 'operation_type', 'transaction_amount')
