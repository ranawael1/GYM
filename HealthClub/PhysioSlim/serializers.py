import imp
from rest_framework import serializers
from django.contrib.auth.models import User 
from .models import *
from .models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'age', 'avatar', 'gender', 'phone']
