import imp
from rest_framework import serializers
<<<<<<< HEAD
from django.contrib.auth.models import User 
from .models import *


class Usererializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
=======
from .models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'age', 'avatar', 'gender', 'phone']
>>>>>>> f457ee587af00c656df43e41c70279c6f78e2d98
