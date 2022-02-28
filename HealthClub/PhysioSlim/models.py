from django.contrib.auth.models import AbstractUser
from django.db import models
<<<<<<< HEAD
from django.contrib.auth.models import User
=======
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
>>>>>>> f457ee587af00c656df43e41c70279c6f78e2d98
