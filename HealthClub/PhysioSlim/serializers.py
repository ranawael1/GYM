from rest_framework import serializers
from .models import Clinic, User, Branch, Offer, Event,PersonalTrainer
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


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ('__all__')

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('__all__')



class PersonalTrainerSerializers(serializers.ModelSerializer):
    class Meta:
        model = PersonalTrainer
        fields = ('__all__')




class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'



class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'

# class CheckSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Check
#         fields = ['id','username', 'age', 'avatar', 'gender', 'phone']