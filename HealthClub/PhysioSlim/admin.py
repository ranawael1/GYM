from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Branch,Offer,Event, Clinic

class ClinicAdmin(admin.ModelAdmin):
    list_display = ('clinic', 'branch')

admin.site.register(User, UserAdmin)
admin.site.register(Branch)
admin.site.register(Offer)
admin.site.register(Event)
admin.site.register(Clinic,ClinicAdmin)