from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,branch,Offer

admin.site.register(User, UserAdmin)
admin.site.register(branch)
admin.site.register(Offer)
