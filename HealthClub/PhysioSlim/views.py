from django.shortcuts import render
from django.contrib.auth.models import Group, User #User model to access users and admins
from .serializers import Usererializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['GET'])
def all(request):
    all= User.objects.all()
    st = Usererializer(all, many=True)
    return Response(st.data)

