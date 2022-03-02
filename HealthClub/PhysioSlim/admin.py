from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Branch,Offer,PersonalTrainer

admin.site.register(User, UserAdmin)
admin.site.register(Branch)
admin.site.register(Offer)
admin.site.register(PersonalTrainer)
