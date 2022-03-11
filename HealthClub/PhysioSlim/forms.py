from dataclasses import Field
import imp
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.shortcuts import redirect
from .models import User, Branch, Offer, Event, Clinic
from .  import verify
import random

#a modified UserCreationForm so we can add a new field(email)
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone','picture', 'age', 'gender' , 'branch', 'membership_num']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.TextInput(attrs={'class': 'form-control'}),
            'password2': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-control'}),
            }

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone','picture', 'age', 'membership_num']
        help_texts = {
            'password ':(''),
        }
  
    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        print(username)
        if email and User.objects.filter(email=email).exclude(username=username).count():
            pass
        else:
            try:
                User.objects.get(email=email)
                raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
            except:
                pass
        return email
    check_phone = False
    def clean_phone(self):
        username = self.cleaned_data.get('username')
        phone = self.cleaned_data.get('phone')
        if phone and User.objects.filter(phone=phone).exclude(username=username).count():
            pass
        else:
            try:
                User.objects.get(phone=phone)
                raise forms.ValidationError('This phone number is already in use. Please supply a different phone.')
            except:
                verify.send(phone)
                global check_phone
                check_phone = True
        return phone

    def save(self, commit=True):
        user = super(EditUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
        if check_phone is True:
            print("checkkk trueee")
            return redirect('verify-code')
        return user

class activateAccount(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'phone','picture', 'age', 'membership_num','branch', 'gender']
        help_texts = {
            'password ':(''),
        }
    check_phone = False
    def clean_user(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
            pass
        except:
            username = username+random.random(0,9999)
        return username
    
    def clean_phone(self):
        username = self.cleaned_data.get('username')
        phone = self.cleaned_data.get('phone')
        if phone and User.objects.filter(phone=phone).exclude(username=username).count():
            pass
        else:
            try:
                User.objects.get(phone=phone)
                raise forms.ValidationError('This phone number is already in use. Please supply a different phone.')
            except:
                verify.send(phone)
                global check_phone
                check_phone = True
        return phone

    def save(self, commit=True):
        user = super(activateAccount, self).save(commit=False)
        user.phone = self.cleaned_data['phone']
        user.is_activated = True
        if commit:
            user.save()
        if check_phone is True:
            print("checkkk trueee")
            return redirect('verify-code')
        return user

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