from email.policy import default
import imp
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import CharField
from phonenumber_field.modelfields import PhoneNumberField
# import schedule
# import time
GENDER = (
    (None, 'Choose your gender'),
    ('male', 'male'),
    ('female', 'female')
)


class Branch(models.Model):
    name = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=50, null=True)
    phone = PhoneNumberField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    phone = PhoneNumberField(unique=True, null=False, blank=False)
    is_verified = models.BooleanField(default=False)
    age = models.IntegerField()
    gender = models.CharField(choices=GENDER, max_length=20)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE , null= True)
    membership_num = models.CharField(max_length=50, null= True, blank=True)
    
    avatar= models.ImageField(upload_to='avatars/',null=True, default='media/avatars/dp/default.jpg', blank=True)

    REQUIRED_FIELDS = ['age', 'gender', 'phone', 'email']


   
    # def delete_not_verifed_users(self):
    #     print("checkkkkk deleteeeee")
    #     if self.is_verified == False:
    #         self.delete()
    # schedule.every(1).minutes.do(delete_not_verifed_users())
    # while True:
    #         schedule.run_pending()
    #         time.sleep(1)

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


class Offer(models.Model):
    name = models.CharField(max_length=50, null=True)
    num_of_class = models.IntegerField()
    discount = models.FloatField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='offer/', null=True, blank=True)

    def __str__(self):
        return self.name


POSITION = (
    (None, 'Position'),
    ('PT', 'PT'),
    ('floor', 'Floor'),
    ('floor&PT', 'Floor & PT')
)


class PersonalTrainer(models.Model):
    name = models.CharField(max_length=50, null=True)
    bio = models.CharField(max_length=500, null=True)
    years_of_experience = models.IntegerField()
    position = models.CharField(choices=POSITION, max_length=20)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    photo = models.ImageField(
        upload_to='PersonalTrainer/', null=True, blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    event = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=1000, null=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='events/', null=True, blank=True)

    def __str__(self):
        return self.event


class Class(models.Model):
    Class = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=500, null=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='Classes/', null=True, blank=True)

    def __str__(self):
        return self.Class


class Clinic(models.Model):
    clinic = models.CharField(max_length=50, null=False, unique=True)
    description = models.CharField(max_length=1000, null=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='clinics/', null=True, blank=True)

    def __str__(self):
        return self.clinic  


#testing favorites

class ClassSubscribers(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)
    favclass = models.ForeignKey(Class, on_delete=models.CASCADE)
    def __str__(self):
        return self.subscriber


