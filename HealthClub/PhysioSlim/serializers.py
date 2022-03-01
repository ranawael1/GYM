import imp
from rest_framework import serializers
from .models import User
from django.db import models
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email','password', 'age', 'gender', 'phone',)



# class CheckSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Check
#         fields = ['id','username', 'age', 'avatar', 'gender', 'phone']
