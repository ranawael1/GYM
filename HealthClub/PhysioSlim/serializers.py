from rest_framework import serializers
from .models import User,branch,Offer
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    class Meta:
        model = User
        fields = ('id','username', 'email','password', 'age', 'gender', 'phone',)
        

class VerifySerializer(serializers.Serializer):
    code = serializers.CharField()


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