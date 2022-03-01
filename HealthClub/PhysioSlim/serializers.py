from rest_framework import serializers
from .models import User,branch,Offer
from django.db import models
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email','password', 'age', 'gender', 'phone',)



class BranchSerializers(serializers.ModelSerializer):
    class Meta:
        model = branch
        fields = ('__all__')

class OfferSerializers(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('__all__')





# class CheckSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Check
#         fields = ['id','username', 'age', 'avatar', 'gender', 'phone']