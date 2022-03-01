from enum import unique
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import CharField
from phonenumber_field.modelfields import PhoneNumberField

GENDER = (
(None, 'Choose your gender'),
('male', 'male'),
('female', 'female')
)
class User(AbstractUser):
    phone = PhoneNumberField(unique = True, null = False, blank = False)
    is_verified = models.BooleanField(default=False)
    age = models.IntegerField()
    gender = models.CharField(choices=GENDER, max_length=20)
    avatar= models.ImageField(upload_to='avatars/')

    REQUIRED_FIELDS = ['age', 'gender']

# class Check(models.Model):
#     phone = PhoneNumberField(unique = True, null = False, blank = False)
#     is_verified = models.BooleanField(default=False)

class branch(models.Model):
    name = models.CharField(max_length=50, null= True)
    address = models.CharField(max_length=50, null= True)

    def __str__(self):
        return self.name 
