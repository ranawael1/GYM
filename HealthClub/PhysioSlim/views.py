import email
import imp
from django.http import HttpResponse
from importlib.resources import contents
from django.shortcuts import redirect, render
from .models import User,Branch,Offer,Event,Class, Clinic
# decorators and authentication
from.decorators import unauthenticated_user
from .models import User,Branch,Offer,PersonalTrainer
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser
from urllib.parse import urlparse
from urllib import parse
from django.contrib import messages
# from .decorators import verification_required  
#forms
from .forms import ClinicForm, CreateUserForm, VerifyForm, EventForm
from channels.layers import get_channel_layer
#Notifications
import json
from django.template import RequestContext
from asgiref.sync import async_to_sync

#home
# def home(request):
#     branches = Branch.objects.all()
#     context={'branches':branches}
#     return render(request, 'physio-slim/base.html', context)
def home(request):
    return render(request, 'physio-slim/home.html', {'room_name' : "broadcast"})

#test notifications
def test(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_broadcast",
        {
            'type': 'send_notification',
            'message': json.dumps("Notification")
        }
    )
    return HttpResponse("Done")
    
#logout
def logoutUser(request):
    logout(request)
    # return redirect(request.META.get('HTTP_REFERER'))  #to stay in the same page after logging out
    
    return redirect('login')

#register
@unauthenticated_user
def register(request):
    form = CreateUserForm()
    print(form)
    if request.method == 'POST':
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            phone = form.cleaned_data.get('phone')
            try:
                verify.send(phone)
            except:
                error = {
                        "error":{
                        "statusCode": 429,
                            "message": "Rate limit is exceeded. Try again later" 
                        }
                    }
                context = {'form':form}
                return render(request, 'physio-slim/register.html', context)
            return redirect('verify', user=user)
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

# def verify_code(request, user):
#     if request.method == 'POST':
#         form = VerifyForm(request.POST)
#         context = {'form': form}
#         if form.is_valid():
#             code = form.cleaned_data.get('code')
#             phone = user.phone
#             try:
#                 x=verify.check(user.phone, code)
#                 if x is not False:
#                     user.save()
#                     return redirect('users')
#                 else:
#                     return render(request, 'physio-slim/verify.html', context)
#             except:
#                 return render(request, 'physio-slim/verify.html', context)
#         context = {'form': form}
#         return render(request, 'physio-slim/verify.html', context)
#     else:
#         form = VerifyForm()
#         context = {'form': form}
#         return render(request, 'physio-slim/verify.html', context)



#login
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        #gather the username and the password entered on the login form
        username = request.POST.get('username')
        password = request.POST.get('password')

        #authenticate the data entered by the user
        user = authenticate(request, username=username, password=password)
        #if the user exists
        if user is not None:
            login(request, user)
            if request.GET.get('next') is not None:
                return redirect(request.GET.get('next'))
            else:
            # return redirect(request.META.get('HTTP_REFERER'), history = -2)  #to stay in the same page after logging in
                return redirect('home')
        #if not, show this flash message
        else:
            messages.info(request, 'Username or Password is incorrect')
    #displaying the loging form
    context ={}
    return render(request, 'physio-slim/login.html', context)


#add clinic form for testing
def addingClinic(request):
    if request.method == 'POST':
        form = ClinicForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all-events')
    else:
        form = ClinicForm()
        return render(request, 'physio-slim/addClinicForm.html', {'form' : form})

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

