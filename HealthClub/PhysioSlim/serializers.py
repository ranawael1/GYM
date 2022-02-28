import imp
from rest_framework import serializers
from django.contrib.auth.models import User 
from .models import *


class Usererializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']