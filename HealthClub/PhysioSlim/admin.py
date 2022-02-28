from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

<<<<<<< HEAD

# Register your models here.
=======
admin.site.register(User, UserAdmin)
>>>>>>> f457ee587af00c656df43e41c70279c6f78e2d98
