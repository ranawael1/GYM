from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User
#a modified UserCreationForm so we can add a new field(email)
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'age', 'gender', 'phone']

class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, help_text='Enter code')

# class CheckForm(forms.ModelForm):
#     class Meta:
#         model = Check
#         fields = ('phone',)