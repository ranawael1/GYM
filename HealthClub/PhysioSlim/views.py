<<<<<<< HEAD
import email
from importlib.resources import contents
from multiprocessing import context
=======
from django.http import HttpResponse
from importlib.resources import contents
>>>>>>> 99b6fc756c4cf76802b963126bb66bc30c6f786a
from django.shortcuts import redirect, render
from .models import User,Branch,Offer,Event
# decorators and authentication
from.decorators import unauthenticated_user
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
# from .decorators import verification_required  
#forms
from .forms import CreateUserForm, VerifyForm, EventForm
#rest_framework imports
from rest_framework.response import Response # like render
from rest_framework.decorators import api_view
from .serializers import UserSerializer,BranchSerializer,OfferSerializer,EventSerializer,VerifySerializer
from . import verify



from rest_framework.views import exception_handler
from rest_framework import status


#logout
def logoutUser(request):
    logout(request)
    # return redirect(request.META.get('HTTP_REFERER'))  #to stay in the same page after logging out
    
    return redirect('login')

@login_required(login_url='login')
# @verification_required  
@api_view(['GET'])
def users(request):
    users = User.objects.all()
    users_ser = UserSerializer(users, many=True)
    return Response(users_ser.data)
    
@login_required(login_url='login')
@api_view(['GET'])
def user(request, user_id):
    user = User.objects.get(id = user_id)
    user_ser = UserSerializer(user, many=False)
    return Response(user_ser.data)

@api_view(['POST'])
def add_user(request):
    user_ser = UserSerializer(data=request.data)
    if user_ser.is_valid():
        valid = user_ser._validated_data
        username= valid.get('username')
        phone=valid.get('phone')
        email = valid.get('email')
        password = make_password(valid.get('password'))
        age = valid.get('age')
        gender = gender =valid.get('gender')
        user_data = {'username': username,'email': email,'password': password, 'phone': phone, 'age': age, 'gender': gender}
        try:
            verify.send(phone)
        except:
            error = {
                    "error":{
                    "statusCode": 429,
                        "message": "Rate limit is exceeded. Try again later" 
                    }
                }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        return redirect("verify-code-api", user=user_data)
    return Response(user_ser.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(["POST"])   
def verify_code_api(request, user):
    if request.method == 'POST':
        user = eval(str(user))
        form = VerifySerializer(data=request.data)
        if form.is_valid():
            valid = form._validated_data
            code = valid.get('code')
            phone = user['phone']
            try:
                x = verify.check(phone, code)
                new_user = User.objects.create( email=user['email'],
                username=user['username'],
                age=user['age'],
                gender =user['age'],
                phone=user['phone'],
                is_verified=True)
                new_user.save()
                return redirect('users')
            except:
                return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def edit_user(request, user_id):
    user = User.objects.get(id=user_id)
    user_ser = UserSerializer(data=request.data, instance=user)
    if user_ser.is_valid():
        user_ser.save()
        return redirect("users")
    return Response(user_ser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
def del_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect("users")


@unauthenticated_user
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

# def verify_code(request):
#     if request.method == 'POST':
#         form = VerifyForm(request.POST)
#         if form.is_valid():
#             code = form.cleaned_data.get('code')
#             phone = request.user.phone
#             if verify.check(request.user.phone, code):
#                 request.user.is_verified = True
#                 request.user.save()
#                 return redirect('users')
#     else:
#         form = VerifyForm()
#         context = {'form': form}
#     return render(request, 'physio-slim/verify.html', context)
# def verify_code(request):
#     if request.method == 'POST':
#         form = VerifyForm(request.POST)
#         if form.is_valid():
#             code = form.cleaned_data.get('code')
#             phone = request.user.phone
#             if verify.check(request.user.phone, code):
#                 request.user.is_verified = True
#                 request.user.save()
#                 return redirect('users')
#     else:
#         form = VerifyForm()
#         context = {'form': form}
#         return render(request, 'physio-slim/verify.html', context)

@unauthenticated_user
def login_user(request):
    print("valid")
    if request.method == 'POST':
        username = request.POST.get('username' )
        password = request.POST.get('password')
        print("valid")
       
        print(username)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return render(request, 'physio-slim/home.html')
        else:
          return render(request, 'physio-slim/register.html')
    else:
      context ={}
      return render(request, 'physio-slim/login.html', context)

def logoutuser(request):
    logout(request)
    
    return redirect('login')


@login_required(login_url='login')
#BranchSerializers
@api_view(['GET'])
def all_branch(request):
    all_branch = Branch.objects.all()
    br_ser = BranchSerializer(all_branch, many=True)
    return Response(br_ser.data)

@login_required(login_url='login')
@api_view(['GET'])
def one_branch(request,br_id):
    br = Branch.objects.get(id=br_id)
    br_ser = BranchSerializer(br,many=False)
    return Response(br_ser.data)

@login_required(login_url='login')
@api_view(['POST'])
def add_branch(request):
    br_ser = BranchSerializer(data=request.data)
    if br_ser.is_valid():
        br_ser.save()
        return redirect('api-all')


        
@login_required(login_url='login')
@api_view(['POST'])
def edit_branch(request,br_id):
    br = Branch.objects.get(id=br_id)
    br_ser = BranchSerializer(data=request.data, instance=br)
    if br_ser.is_valid():
        br_ser.save()
        return redirect('api-all')



@login_required(login_url='login')
@api_view(['DELETE'])
def del_branch(request,br_id):
    br = Branch.objects.get(id=br_id)
    br.delete()
    return Response('branch Deleted Success')


#OfferSerializers
@api_view(['GET'])
def all_Offer(request):
    all_Offer = Offer.objects.all()
    of_ser = OfferSerializer(all_Offer, many=True)
    return Response(of_ser.data)

@api_view(['GET'])
def one_Offer(request,of_id):
    of = Offer.objects.get(id=of_id)
    of_ser = OfferSerializer(of,many=False)
    return Response(of_ser.data)

@api_view(['POST'])
def add_Offer(request):
    of_ser = OfferSerializer(data=request.data)
    if of_ser.is_valid():
        of_ser.save()
        return redirect('api-all')
        

@api_view(['POST'])
def edit_Offer(request,of_id):
    of = Offer.objects.get(id=of_id)
    of_ser = OfferSerializer(data=request.data, instance=of)
    if of_ser.is_valid():
        of_ser.save()
        return redirect('api-all')

@api_view(['DELETE'])
def del_Offer(request,of_id):
    of = Offer.objects.get(id=of_id)
    of.delete()
    return Response('Offer Deleted Success')



# Events API
#display all events
@api_view(['GET'])
def allEvents(request):
    all_ev = Event.objects.all()
    all_events = EventSerializer(all_ev, many=True)
    return Response(all_events.data)


# displaying the events of a certain branch
@api_view(['GET'])
def showBranchEvents(request, br_id):
    branch_ev = Event.objects.filter(branch_id=br_id)
    branch_events = EventSerializer(branch_ev, many=True)
    return Response(branch_events.data)

#adding an event to a certain branch
@api_view(['POST'])
def addEvent(request):
    added_event = EventSerializer(data=request.data)
    if added_event.is_valid():
        added_event.save()
        return redirect ('all-events')


#edit event
@api_view(['POST'])
def editEvent(request, ev_id):
    event = Event.objects.get(id=ev_id)
    event_ser = EventSerializer(data=request.data, instance=event)
    if event_ser.is_valid():
        event_ser.save()
        return redirect ('all-events')

#delete event
@api_view(['DELETE'])
def delEvent(request,ev_id):
    event = Event.objects.get(id=ev_id)
    event.delete()
    return HttpResponse ('Event deleted')

#add event form for testing
def addingEvent(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all-events')
    else:
        form = EventForm()
        return render(request, 'physio-slim/addeventform.html', {'form' : form})




