from importlib.resources import contents
from multiprocessing import context
from django.shortcuts import redirect, render
from .models import User,branch,Offer
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout

from .forms import CreateUserForm, VerifyForm
#rest_framework imports
from rest_framework.response import Response # like render
from rest_framework.decorators import api_view
from .serializers import UserSerializer,BranchSerializers,OfferSerializers
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

def login_2(request):
    print("valid")
    if request.method == 'POST':
        username = request.POST.get('username' )
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return render(request, 'physio-slim/home.html')
        else:
          return render(request, 'physio-slim/register.html')
    else:
      context ={}
      return render(request, 'physio-slim/login.html', context)


#BranchSerializers
@api_view(['GET'])
def all_branch(request):
    all_branch = branch.objects.all()
    br_ser = BranchSerializers(all_branch, many=True)
    return Response(br_ser.data)

@api_view(['GET'])
def one_branch(request,br_id):
    br = branch.objects.get(id=br_id)
    br_ser = BranchSerializers(br,many=False)
    return Response(br_ser.data)

@api_view(['POST'])
def add_branch(request):
    br_ser = BranchSerializers(data=request.data)
    if br_ser.is_valid():
        br_ser.save()
        return redirect('api-all')
        

@api_view(['POST'])
def edit_branch(request,br_id):
    br = branch.objects.get(id=br_id)
    br_ser = BranchSerializers(data=request.data, instance=br)
    if br_ser.is_valid():
        br_ser.save()
        return redirect('api-all')

@api_view(['DELETE'])
def del_branch(request,br_id):
    br = branch.objects.get(id=br_id)
    br.delete()
    return Response('branch Deleted Success')


#OfferSerializers
@api_view(['GET'])
def all_Offer(request):
    all_Offer = Offer.objects.all()
    of_ser = OfferSerializers(all_Offer, many=True)
    return Response(of_ser.data)

@api_view(['GET'])
def one_Offer(request,of_id):
    of = Offer.objects.get(id=of_id)
    of_ser = OfferSerializers(of,many=False)
    return Response(of_ser.data)

@api_view(['POST'])
def add_Offer(request):
    of_ser = OfferSerializers(data=request.data)
    if of_ser.is_valid():
        of_ser.save()
        return redirect('api-all')
        

@api_view(['POST'])
def edit_Offer(request,of_id):
    of = Offer.objects.get(id=of_id)
    of_ser = OfferSerializers(data=request.data, instance=of)
    if of_ser.is_valid():
        of_ser.save()
        return redirect('api-all')

@api_view(['DELETE'])
def del_Offer(request,of_id):
    of = Offer.objects.get(id=of_id)
    of.delete()
    return Response('Offer Deleted Success')


