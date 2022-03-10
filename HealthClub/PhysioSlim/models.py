from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.core.validators import FileExtensionValidator
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
class Branch(models.Model):
    name = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=150, null=True)
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
    is_subscribed = models.BooleanField(default=False)
    avatar= models.ImageField(upload_to='avatars/',null=True, default='static/avatars/default.jpg', blank=True)

    REQUIRED_FIELDS = ['age', 'gender', 'phone', 'email']


   
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

class Class(models.Model):
    Class = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=500, null=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
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
        ordering = ('-id',)

        

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


class Gallery(models.Model):
    name = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=1000, null=True)
    img = models.ImageField(upload_to='gallery/')
    def __str__(self):
        return self.name
    
