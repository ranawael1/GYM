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
    #avatar= models.ImageField(upload_to='avatars/')



    REQUIRED_FIELDS = ['age', 'gender']

# class Check(models.Model):
#     phone = PhoneNumberField(unique = True, null = False, blank = False)
#     is_verified = models.BooleanField(default=False)

# class Check(models.Model):
#     phone = PhoneNumberField(unique = True, null = False, blank = False)
#     is_verified = models.BooleanField(default=False)
#     age = models.IntegerField()
#     gender = models.CharField(choices=GENDER, max_length=20)
#     avatar= models.ImageField(upload_to='avatars/')
#     username = models.CharField(max_length=50)
class Branch(models.Model):
    name = models.CharField(max_length=50, null= True)
    address = models.CharField(max_length=50, null= True)

    def __str__(self):
        return self.name 

class Offer(models.Model):
    name = models.CharField(max_length=50, null = True)
    num_of_class = models.IntegerField()
    discount = models.FloatField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    def __str__(self):
        return self.name 
class Train(models.Model):
    train = models.CharField(max_length=50, null= True)

class PersonalTrainer(models.Model):
    name = models.CharField(max_length=50, null= True)
    bio = models.CharField(max_length=500, null= True)
    year_of_exprince = models.IntegerField()
    train_name = models.ForeignKey(Train ,on_delete=models.CASCADE)
    branch_name = models.ForeignKey(Branch ,on_delete=models.CASCADE)
    def __str__(self):
        return self.track_name

class Event(models.Model):
    event = models.CharField(max_length=50, null = False)
    description = models.CharField(max_length=500, null = False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='events/', null = True, blank=True)
    def __str__(self):
        return self.event 
