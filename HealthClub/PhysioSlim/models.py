from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

GENDER = (
(None, 'Choose your gender'),
('male', 'male'),
('female', 'female')
)
class User(AbstractUser):
    phone = PhoneNumberField(unique = True, null = False, blank = False) # Here
    age = models.IntegerField()
    gender = models.CharField(choices=GENDER, max_length=20)
    avatar= models.ImageField(upload_to='avatars/')

    REQUIRED_FIELDS = ['age', 'gender']