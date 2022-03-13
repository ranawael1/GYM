from csv import list_dialects
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
<<<<<<< HEAD
from .models import Class_days, User,Branch,Offer,PersonalTrainer,Event,Clinic, Class,ClassSubscribers ,Notifications,Gallery,MainOffer,Schedule
=======
from .models import User,Branch,Offer,PersonalTrainer,Event,Clinic, Class,ClassSubscribers ,Notifications,Gallery,MainOffer, EventParticipants
>>>>>>> 41d250fe752d3f8d3711f44568f8d79234cafe52

class ClinicAdmin(admin.ModelAdmin):
    list_display = ('clinic', 'branch')

class TrainerAdmin(admin.ModelAdmin):
    list_display = ('name','years_of_experience','position')

class UsersAdmin(admin.ModelAdmin):
    list_display = ('username','is_superuser','phone','is_subscribed','gender','branch','membership_num', 'email')

class ClassSubscribersAdmin(admin.ModelAdmin):
    list_display = ('subscriber','favclass')

class ClassAdmin(admin.ModelAdmin):
    list_display = ('Class','branch')

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('classes','day','branch' , 'From','To')

class EventParticipantsAdmin(admin.ModelAdmin):
    list_display = ('participant','event')



admin.site.register(User,UsersAdmin)
admin.site.register(EventParticipants, EventParticipantsAdmin)
admin.site.register(Branch)
admin.site.register(Offer)
admin.site.register(Event)
admin.site.register(Class_days)
admin.site.register(Schedule,ScheduleAdmin)
admin.site.register(Class,ClassAdmin)
admin.site.register(Clinic,ClinicAdmin)
admin.site.register(PersonalTrainer,TrainerAdmin)
admin.site.register(Notifications)
admin.site.register(ClassSubscribers,ClassSubscribersAdmin)
admin.site.register(Gallery)
admin.site.register(MainOffer)

