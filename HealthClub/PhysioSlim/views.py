from importlib.resources import contents
from multiprocessing import context
from django.shortcuts import redirect, render
from .models import User
from .forms import CreateUserForm, VerifyForm
#rest_framework imports
from rest_framework.response import Response # like render
from rest_framework.decorators import api_view
from rest_framework import validators
from .serializers import UserRegistrationSerializer, UserSerializer, CheckSerializer
from . import verify
from django.contrib.auth.decorators import login_required
from .decorators import verification_required  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password


#@verification_required  
@api_view(['GET'])
def users(request):
    users = User.objects.all()
    users_ser = UserSerializer(users, many=True)
    return Response(users_ser.data)

@api_view(['GET'])
def user(request, user_id):
    user = User.objects.get(id = user_id)
    user_ser = UserSerializer(user, many=False)
    return Response(user_ser.data)

@api_view(['POST'])
def add_user(request):
    print("before")
    user_ser = UserSerializer(data=request.data)
    print("after")
    if user_ser.is_valid():
        valid = user_ser._validated_data
        user = User.objects.create( email=valid.get('email'),
        username=valid.get('username'),
        password = make_password(valid.get('password')),
        age=valid.get('age'),
        gender =valid.get('gender'),
        phone=valid.get('phone')
        )
        user.save()
    else:
        print(user_ser.errors)
    return redirect("users")
    

def register(request):
    form = CreateUserForm()
    print(form)
    if request.method == 'POST':
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            pp = form.cleaned_data.get('avatar')
            print(pp)
            phone = form.cleaned_data.get('phone')
            login(request, user)  # go to login page later
            # verify.send(phone)
            return redirect('users')
    context = {'form':form}
    return render(request, 'physio-slim/register.html', context)

def verify_code(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            phone = request.user.phone
            if verify.check(request.user.phone, code):
                request.user.is_verified = True
                request.user.save()
                return redirect('users')
    else:
        form = VerifyForm()
        context = {'form': form}
    return render(request, 'physio-slim/verify.html', context)