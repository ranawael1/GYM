import imp
from math import pi
from urllib import request
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import MultipleHiddenInput
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.core.signals import request_finished
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
import urllib.parse as urlparse
from urllib.request import urlopen
from io import BytesIO
import os
from django.core.files import File

# import schedule
# import time
GENDER = (
    (None, 'Choose your gender'),
    ('male', 'male'),
    ('female', 'female')
)

POSITION = (
    (None, 'Position'),
    ('PT', 'PT'),
    ('floor', 'Floor'),
    ('floor&PT', 'Floor & PT')
)

DAYS = (
    (None, 'chosse your training days'),
    ('1 day ', '1 day'),
    ('2 days ', '2 days'),
    ('3 days ', '3 days'),
    ('4 days ', '4 days'),
    ('5 days ', '5 days'),
    ('6 days ', '6 days'),
    ('Everyday', 'Everyday'),
)
# WEEKDAYS= (
#     (None, 'chosse the class days'),
#     ('Saturday', 'Saturday'),
#     ('Sunday', 'Sunday'),
#     ('Monday ', 'Monday'),
#     ('Tuesday ', 'Tuesday'),
#     ('Wednesday', 'Wednesday'),
#     ('Thursday', 'Thursday'),
#     ('Friday', 'Friday'),
# )
class Branch(models.Model):
    name = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=150, null=True)
    phone = PhoneNumberField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    phone = PhoneNumberField(unique=True, null=False, blank=False)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=True)
    age = models.DateTimeField(default=None, null=True)
    gender = models.CharField(choices=GENDER, max_length=20)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE , null= True)
    membership_num = models.CharField(max_length=50, null= True, blank=True)
    is_subscribed = models.BooleanField(default=False)
    picture= models.ImageField(upload_to='avatars/',null=True, default='static/profile/default.jpg', blank=True, max_length=1000)


    REQUIRED_FIELDS = ['phone', 'email']

    @receiver(user_signed_up)
    def populate_profile(sociallogin, user, **kwargs):

        user.profile = User()

        # if sociallogin.account.provider == 'facebook':
        #     user_data = user.socialaccount_set.filter(provider='facebook')[0].extra_data
        #     picture_url = "http://graph.facebook.com/" + sociallogin.account.uid + "/picture?type=large"
        #     email = user_data['email']
        #     full_name = user_data['name']

        if sociallogin.account.provider == 'google':
            print("goooooooooogle")
            user_data = user.socialaccount_set.filter(provider='google')[0].extra_data
            print('goooooooooogle tany')
            picture_url = user_data['picture']

            email = user_data['email']
            print(picture_url)
        user.email = email
        user.is_activated = False
        avatar = urlopen(picture_url)
        
        from django.template.defaultfilters import slugify
        from django.core.files.base import ContentFile
        user.picture.save(slugify(user.username + " social") + '.jpg', 
                ContentFile(avatar.read()))
        user.save()

    # def delete_not_verifed_users(self):
    #     print("checkkkkk deleteeeee")
    #     if self.is_verified == False:
    #         self.delete()
    # schedule.every(1).minutes.do(delete_not_verifed_users())
    # while True:
    #         schedule.run_pending()
    #         time.sleep(1)


class Offer(models.Model):
    name = models.CharField(max_length=50, null=True)
    num_of_class = models.IntegerField()
    discount = models.IntegerField()
    days_num = models.CharField(choices=DAYS, max_length=20,null=True)
    number_of_months= models.IntegerField(null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE )
    photo = models.ImageField(upload_to='offer/', null=True, blank=True )
    created_on = models.DateTimeField(default=timezone.now)
    due = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)


    def save(self,*args,**kwargs):
        users = User.objects.all()
        created = not self.id
        super().save(*args,**kwargs)
        if created :
            notification = Notifications.objects.create(notification_type=4,Offer=self)
            notification.to_user.set(users)
            notification.save()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_on',)

class MainOffer(models.Model):
    name = models.CharField(max_length=50, null=True)
    num_of_class = models.IntegerField()
    discount = models.IntegerField()
    days_num = models.CharField(choices=DAYS, max_length=20, null=True)
    number_of_months= models.IntegerField(null=True)
    photo = models.ImageField(upload_to='offer/', null=True, blank=True )
    created_on = models.DateTimeField(default=timezone.now)
    due = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    def save(self,*args,**kwargs):
        users = User.objects.all()
        created = not self.id
        super().save(*args,**kwargs)
        if created :
            notification = Notifications.objects.create(notification_type=5,MainOffer=self)
            notification.to_user.set(users)
            notification.save()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_on',)


class PersonalTrainer(models.Model):
    name = models.CharField(max_length=50, null= True)
    bio = models.CharField(max_length=500, null= True)
    years_of_experience = models.IntegerField()
    position = models.CharField(choices=POSITION, max_length=20)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='PersonalTrainer/', null=True, blank=True)

    def save(self,*args,**kwargs):
        users = User.objects.all()
        created = not self.id
        super().save(*args,**kwargs)
        if created :
            notification = Notifications.objects.create(notification_type=3,trainer=self)
            notification.to_user.set(users)
            notification.save()

    def __str__(self):
        return self.name


class Event(models.Model):
    event = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=1000, null=False)
    photo = models.ImageField(upload_to='events/', null=True, blank=True)
    num_of_participants = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now)
    due = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    def save(self,*args,**kwargs):
        users = User.objects.all()
        created = not self.id
        super().save(*args,**kwargs)
        if created :
            notification = Notifications.objects.create(notification_type=2,Event=self)
            notification.to_user.set(users)
            notification.save()

    def __str__(self):
        return self.event
    
    class Meta:
        ordering = ('-created_on',)
    

class EventParticipants(models.Model):
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)




class Notifications(models.Model):
    #1=class, 2=event, 3 =trainer , 4=offer , 5=main offer
    notification_type = models.IntegerField()
    to_user = models.ManyToManyField(User,related_name='to_user',blank=True)
    trainer = models.ForeignKey(PersonalTrainer,related_name='PersonalTrainer', on_delete=models.CASCADE, null=True)
    Class = models.ForeignKey('Class',on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    Event = models.ForeignKey('Event',on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    Offer = models.ForeignKey('Offer',on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    MainOffer = models.ForeignKey('MainOffer',on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    created_on = models.DateTimeField(default=timezone.now)
    user_seen = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_on',)

class Working_days(models.Model):
    class_days = models.CharField(max_length=20, default=None)
    def __str__(self):
        return self.class_days  
    class Meta:
        ordering = ('id',)

class Class(models.Model):
    Class = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=500, null=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    # class_days = models.ManyToManyField(Class_days, related_name='Class_days', blank=True)
    photo=models.ImageField(upload_to='Classes/', null=True, blank=True )
    icon = models.FileField(upload_to='Classes/', null=True, blank=True , default='static/avatars/default.jpg' ,validators=[FileExtensionValidator(['jpg', 'svg'])])

    def save(self,*args,**kwargs):
        users = User.objects.all()
        created = not self.id
        super().save(*args,**kwargs)
        if created :
            notification = Notifications.objects.create(notification_type=1,Class=self)
            notification.to_user.set(users)
            notification.save()
    class Meta:
        ordering = ('id',)



    def __str__(self):
        return self.Class


class Clinic(models.Model):
    clinic = models.CharField(max_length=50, null=False, unique=True)
    description = models.CharField(max_length=1000, null=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='clinics/', null=True, blank=True)

    def __str__(self):
        return self.clinic

    class Meta:
        ordering = ('-id',)


#testing favorites
class ClassSubscribers(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)
    favclass = models.ForeignKey(Class, on_delete=models.CASCADE)
    # def __str__(self):
    #     return self.subscriber
    # def __str__(self):
    #     return self.favclass


class Schedule(models.Model):
    day = models.ForeignKey(Working_days , on_delete=models.CASCADE)
    classes =models.ForeignKey(Class , on_delete=models.CASCADE)
    branch =models.ForeignKey(Branch , on_delete=models.CASCADE)
    From = models.TimeField()
    To = models.TimeField()
    class Meta:
        ordering = ('day',)
    
   




class Gallery(models.Model):
    name = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=1000, null=True)
    img = models.ImageField(upload_to='gallery/')
    def __str__(self):
        return self.name
    
