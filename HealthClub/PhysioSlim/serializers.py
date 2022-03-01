import imp
from rest_framework import serializers
from django.contrib.auth.models import User 
from .models import *
from .models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'password', 'age', 'avatar', 'gender', 'phone']


class BranchSerializers(serializers.ModelSerializer):
    class Meta:
        model = branch
        fields = ('__all__')