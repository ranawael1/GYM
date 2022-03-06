from dataclasses import Field
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Branch, Offer, Event, Clinic
#a modified UserCreationForm so we can add a new field(email)
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone','avatar', 'age', 'gender' , 'branch', 'membership_num']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.TextInput(attrs={'class': 'form-control'}),
            'password2': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-control'}),
            }

class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, help_text='Enter code')

# class CheckForm(forms.ModelForm):
#     class Meta:
#         model = Check
#         fields = ('phone',)
class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ('name', 'address')
        widgets = { 'name': forms.TextInput(attrs={'class': 'form-control'}), 'address': forms.TextInput(attrs={'class': 'form-control'})}


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('name', 'num_of_class','discount')
        widgets = { 'name': forms.TextInput(attrs={'class': 'form-control'}), 'num_of_class': forms.NumberInput(attrs={'class': 'form-control'}),'discount': forms.NumberInput(attrs={'class': 'form-control'}) }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('__all__')


class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = ('__all__')