from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Branch,Offer,PersonalTrainer,Event,Clinic, Class, Notifications

class ClinicAdmin(admin.ModelAdmin):
    list_display = ('clinic', 'branch')

class TrainerAdmin(admin.ModelAdmin):
    list_display = ('name','years_of_experience','position')

class UsersAdmin(admin.ModelAdmin):
    list_display = ('username','is_superuser','phone','gender','branch','membership_num', 'email')

admin.site.register(User,UsersAdmin)

admin.site.register(Branch)
admin.site.register(Offer)
admin.site.register(Event)
admin.site.register(Class)
admin.site.register(Clinic,ClinicAdmin)
admin.site.register(PersonalTrainer,TrainerAdmin)
admin.site.register(Notifications)
