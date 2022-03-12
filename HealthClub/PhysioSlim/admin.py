from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Class_days, User,Branch,Offer,PersonalTrainer,Event,Clinic, Class,ClassSubscribers ,Notifications,Gallery,MainOffer, sechdule

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

class scheduleAdmin(admin.ModelAdmin):
    list_display = ('day','classes','branch' , 'From','To')




admin.site.register(User,UsersAdmin)

admin.site.register(Branch)
admin.site.register(Offer)
admin.site.register(Event)
admin.site.register(Class_days)
admin.site.register(sechdule,scheduleAdmin)
admin.site.register(Class,ClassAdmin)
admin.site.register(Clinic,ClinicAdmin)
admin.site.register(PersonalTrainer,TrainerAdmin)
admin.site.register(Notifications)
admin.site.register(ClassSubscribers,ClassSubscribersAdmin)
admin.site.register(Gallery)
admin.site.register(MainOffer)

