from . import verify
import email
import imp

from multiprocessing import context
from importlib.resources import contents
from django.shortcuts import redirect, render
from .models import User, Branch, Offer, Event, Class, Clinic, PersonalTrainer, ClassSubscribers, Notifications,Gallery
# decorators and authentication
from .decorators import unauthenticated_user, unverified_user
# send email
from django.core.mail import send_mail
import re
# forms
from .forms import ClinicForm, CreateUserForm, VerifyForm, EventForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser
from urllib.parse import urlparse
from urllib import parse
from django.contrib import messages
# from .decorators import verification_required
# from rest_framework import permissions
# from rest_framework.views import exception_handler
# from rest_framework import status
from django.http import HttpResponse
from channels.layers import get_channel_layer
# Notifications
import json
from django.template import RequestContext
from asgiref.sync import async_to_sync


#Register
@unverified_user
@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            phone = form.cleaned_data.get('phone')
            try:
                verify.send(phone)
                print("check")
                user.save()
                login(request, user)
            except:
                error = {
                    "error": {
                        "statusCode": 429,
                        "message": "Rate limit is exceeded. Try again later"
                    }
                }
                print(error)
                context = {'form': form}
                return render(request, 'physio-slim/register.html', context)
            return redirect('verify-code')
    context = {'form': form}
    return render(request, 'physio-slim/register.html', context)

#Verify Register
def verify_code(request):
    if request.method == 'POST':

        user = request.user
        form = VerifyForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            code = form.cleaned_data.get('code')
            phone = user.phone
            try:
                print('check verify', phone)
                x = verify.check(phone, code)
                # if x is not False:
                user.is_verified = True
                print('2')
                user.save()
                print('3')
                return redirect('home')

                # else:
                #     return render(request, 'physio-slim/verify.html', context)
            except:
                return render(request, 'physio-slim/verify.html', context)
        context = {'form': form}
        return render(request, 'physio-slim/verify.html', context)
    else:
        form = VerifyForm()
        context = {'form': form}
        return render(request, 'physio-slim/verify.html', context)

#Reverify Register
def reverify_code(request):
    verify.cancellation(request.user.phone)
    form = VerifyForm()
    context = {'form': form}
    return render(request, 'physio-slim/verify.html', context)

#login
@unverified_user
@unauthenticated_user
def loginUser(request):
    if request.method == 'POST':
        # gather the username and the password entered on the login form
        username = request.POST.get('username')
        password = request.POST.get('password')
        # authenticate the data entered by the user
        user = authenticate(request, username=username, password=password)
        print(user)
        # if the user exists
        if user is not None:
            login(request, user)
            if request.GET.get('next') is not None:
                return redirect(request.GET.get('next'))
            else:
                # return redirect(request.META.get('HTTP_REFERER'), history = -2)  #to stay in the same page after logging in
                return redirect('home')
        # if not, show this flash message
        else:
            email = username
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    if request.GET.get('next') is not None:
                        return redirect(request.GET.get('next'))
                    else:
                        # return redirect(request.META.get('HTTP_REFERER'), history = -2)  #to stay in the same page after logging in
                        return redirect('home')
            except:
                messages.info(request, 'Username or Password is incorrect')
    # displaying the loging form
    context = {}
    return render(request, 'physio-slim/login.html', context)


#Logout
def logoutUser(request):
    logout(request)
    # return redirect(request.META.get('HTTP_REFERER'))  #to stay in the same page after logging out
    return redirect('home')

# Home
def home(request):
    gallery = Gallery.objects.all()
    if not request.user.is_anonymous : 
        notifications = UserNotifications(request)
        context = {'gallery' : gallery , 'notifications' : notifications }
    else: 
        context = {'gallery' : gallery }
    return render(request,'physio-slim/index.html', context)
   
#Gallery
def gallery(request):
    gallery = Gallery.objects.all()
    context = {'gallery' : gallery }
    return render(request,'physio-slim/gallery.html', context)

# branch home page 
#Contact Page
def contact(request):
    branches = Branch.objects.all()
    context = { 'branches' : branches }
    return render(request,'physio-slim/contact.html', context)
#About Page
def about(request):
    return render(request,'physio-slim/about.html')
# Branch Page
def branch(request, br_id):
    branch = Branch.objects.get(id=br_id)
    classes = Class.objects.filter(branch=br_id)[0:3]
    print(classes)
    clinics = Clinic.objects.filter(branch=br_id)[0:3]
    offers = Offer.objects.filter(branch=br_id)[0:3]
    events = Event.objects.filter(branch=br_id)[0:3]
    trainers = PersonalTrainer.objects.filter(branch=br_id)[0:3]
    context = {'branch': branch, 'classes': classes,
               'clinics': clinics, 'offers': offers, 'trainers': trainers, 'events': events}
    return render(request, 'physio-slim/branch.html', context)

#######Branch Pages#######
#Classes Branch page
def classes(request, br_id):
    branches = Branch.objects.all()
    branch = Branch.objects.get(id=br_id)
    classes = Class.objects.filter(branch=br_id)
    if not request.user.is_anonymous:
        all_subscribers = ClassSubscribers.objects.filter(subscriber=request.user).values_list('favclass_id', flat=True)
        context = {'classes': classes, 'branch': branch,
                'branches': branches, 'all_subscribers':all_subscribers }
    else:
        context = {'classes': classes, 'branch': branch,
                'branches': branches }
    return render(request, 'physio-slim/classes.html', context)

# to show the Event Detailes
def event_details(request ,br_id ):
    branches=Branch.objects.all()
    branch = Branch.objects.get(id=br_id)
    events= Event.objects.filter(branch=br_id)
    context = {'events': events, 'branch': branch , 'branches':branches}
    return render(request, 'physio-slim/br_eventDetails.html', context)


# subscribe to a Class
def subscribeToClass(request, class_id):
    classs = Class.objects.get(id=class_id)
    classSubscriber = ClassSubscribers.objects.create(subscriber=request.user, favclass=classs)
    branch = request.user.branch_id
    branches = Branch.objects.all()
    context = {'classes': classs, 'branch': branch, 'branches': branches}
    email = request.user.email
    # if the user is subscribed to at least one class, we set is_subscribed to True


    if not request.user.is_subscribed:
        request.user.is_subscribed = True
        request.user.save()
        #send notification of subscription
        # notification = Notifications.objects.create(notification_type=1, from_user=request.user,to_user=classs.user, Class=classs)


    # send email to the management to contact the subscriber
    # send_mail(
    #     'New user subscribed!',
    #     f'The user: {request.user} \n has subscribed to: {classs} class, \n branch: {request.user.branch}, \n phone number:{request.user.phone} ',
    #     'physio.slim2@gmail.com',
    #     ['physio.slim2@gmail.com'],
    #     fail_silently=False,)
    #     # send email confirming subscription
    # send_mail(
    #     'Subscription Successful!',
    #     f'Hello {request.user} Thank you for subscribing to our {classs} class, welcome on board \n you might receive a call from our side to have a further discussion', 
        
    #     'physio.slim2@gmail.com',
    #     [f'{email}'],
    #     fail_silently=False,)
    return redirect('classes', branch)

#display favorite classes
@login_required(login_url='login')
def favoriteClasses(request):
    all_subscribers = ClassSubscribers.objects.filter(subscriber=request.user).values_list('favclass_id', flat=True)
    #getting the classes the user subscribed to
    favorite_classes = ClassSubscribers.objects.filter(subscriber_id=request.user.id).values_list('favclass_id', flat=True)
    #turning it into a list
    fav_classes=list(favorite_classes)
    #getting the info of the favorite classes from the Class Model
    classes = Class.objects.filter(id__in = fav_classes)
    context={'classes':classes, 'all_subscribers':all_subscribers}

    return render(request, 'physio-slim/favorites.html', context)


# Unsubscribe from a class
def unSubscribeFromClass(request, class_id):
    classs = Class.objects.get(id=class_id)
    branch = request.user.branch_id
    branches = Branch.objects.all()
    email = request.user.email
    favclass = ClassSubscribers.objects.get(subscriber=request.user, favclass=classs)
    favclass.delete()
    try:
        subscriber = ClassSubscribers.objects.get(subscriber_id=request.user.id)
    except:
        if request.user.is_subscribed:
            request.user.is_subscribed = False
            request.user.save()
    context = {'classes': classs, 'branch': branch, 'branches': branches}
    # send email to the management to confirm the unsubscription
    # send_mail(
    #     'User unsubscribed!',
    #     f'The user: {request.user} \n unsubscribed from: {classs} class, \n branch: {request.user.branch}, \n phone number:{request.user.phone} ',
    #     'physio.slim2@gmail.com',
    #     ['physio.slim2@gmail.com'],
    #     fail_silently=False,)
    #     # send email confirming the unsubscription
    # send_mail(
    #     'Unsubscription',
    #     f'Hello {request.user},\n sorry to here that you unsubscribed from our {classs} class, \n you might receive a call from our side to have a further discussion \n Br, \n Physio-Slim management.', 
        
    #     'physio.slim2@gmail.com',
    #     [f'{email}'],
    #     fail_silently=False,)

    return redirect('classes', branch)




#Clinics Branch page
def clinics(request, br_id):
    branch = Branch.objects.get(id=br_id)
    clinic = Clinic.objects.filter(branch=br_id)
    print(clinic)
    context = {'clinics': clinic, 'branch': branch}
    return render(request, 'physio-slim/br_clinics.html', context)

#Offers Branch page
def offers(request, br_id):
    branch = Branch.objects.get(id=br_id)
    offers = Offer.objects.filter(branch=br_id)
    context = {'offers': offers, 'branch': branch}
    return render(request, 'physio-slim/br_offer.html', context)

#Trainers Branch page
def trainers(request, br_id):
    branch = Branch.objects.get(id=br_id)
    trainers = PersonalTrainer.objects.filter(branch=br_id)
    context = {'trainers': trainers, 'branch': branch}
    return render(request, 'physio-slim/trainers.html', context)


##Showing notifications

def UserNotifications(request):
    notification = Notifications.objects.filter(to_user = request.user)
    notification.user_seen = True
    return notification

# def showNotifications(request):
#     notification = Notifications.objects.filter(to_user = request.user)
#     context = {'notifications': notifications}
#     return render(request, 'physio-slim/index.html', context)
    

##Redirect to notifications

def ClassNotifications(request,notification_id,class_id):
    notification = Notifications.objects.get(id = notification_id)
    classs = Class.objects.get(id=class_id)
    notification.user_seen = True
    notification.save()
    return render(request, 'physio-slim/classes.html')

def EventNotifications(request,notification_id,event_id):
    notification = Notifications.objects.get(id = notification_id)
    event = Event.objects.get(id = event_id)
    notification.user_seen = True
    notification.save()
    return redirect('home')

def TrainerNotifications(request,notification_id,trainer_id):
    notification = Notifications.objects.get(id = notification_id)
    trainer = PersonalTrainer.objects.get(id = trainer_id)
    notification.user_seen = True
    notification.save()
    return render(request, 'physio-slim/trainers.html')

def OfferNotifications(request,notification_id,offer_id):
    notification = Notifications.objects.get(id = notification_id)
    offer = Offer.objects.get(id = offer_id)
    notification.user_seen = True
    notification.save()
    return redirect('home')

#Removing Notification
def RemoveNotifications(request, notification_id):
    notification = Notifications.objects.get(id = notification_id)  
    notification.user_seen = True
    # notification.remove()
    # notification.delete()
    notification.save()
    HttpResponse('success', content_type='text/plain')
  










# def verify_code(request):
#     if request.method == 'POST':
#         form = VerifyForm(request.POST)
#         if form.is_valid():
#             code = form.cleaned_data.get('code')
#             phone = request.user.phone
#             if verify.check(request.user.phone, code):
#                 request.user.is_verified = True
#                 request.user.save()
#                 return redirect('home')
#     else:
#         form = VerifyForm()
#         context = {'form': form}
#     return render(request, 'physio-slim/verify.html', context)


# @verification_required
# @api_view(['GET'])
# def users(request):
#     users = User.objects.all()
#     users_ser = UserSerializer(users, many=True)
#     return Response(users_ser.data)
#     # user = User.objects.get(id=1)
#     # login(request, user)
#     # check = request.user.is_anonymous
#     # print(check)
#     # users = User.objects.all()
#     # users_ser = UserSerializer(users, many=True)
#     # return Response({'user':users_ser.data, 'check':check})

# @login_required(login_url='login')
# @api_view(['GET'])
# def user(request, user_id):
#     user = User.objects.get(id = user_id)
#     user_ser = UserSerializer(user, many=False)
#     return Response(user_ser.data)

# @api_view(['POST'])
# def add_user(request):
#     user_ser = UserSerializer(data=request.data)
#     print("check")
#     if user_ser.is_valid():
#         print("check2")
#         valid = user_ser._validated_data
#         username= valid.get('username')
#         phone=valid.get('phone')
#         email = valid.get('email')
#         password = make_password(valid.get('password'))
#         age = valid.get('age')
#         gender =valid.get('gender')
#         branch = valid.get('branch')
#         user_data = {'username': username,'email': email,'password': password, 'phone': phone, 'age': age, 'gender': gender, 'branch': branch}
#         try:
#             verify.send(phone)
#         except:
#             error = {
#                     "error":{
#                     "statusCode": 429,
#                         "message": "Rate limit is exceeded. Try again later"
#                     }
#                 }
#             return Response(error, status=status.HTTP_400_BAD_REQUEST)
#         return Response(user_ser.data)
#     print(user_ser.data, user_ser.errors)

#     return Response(user_ser.errors, status=status.HTTP_400_BAD_REQUEST)
# @api_view(["POST"])
# def verify_code_api(request):
#     if request.method == 'POST':
#         params =request.GET.urlencode()
#         # print(params)
#         user= dict(parse.parse_qsl(params))
#         form = VerifySerializer(data=request.data)
#         if form.is_valid():
#             print("ok")
#             valid = form._validated_data
#             code = valid.get('code')
#             phone = user['phone']
#             try:
#                 x = verify.check(phone, code)
#                 if x is not False:
#                     new_user = User.objects.create( email=user['email'],
#                     username=user['username'],
#                     age=user['age'],
#                     gender =user['age'],
#                     phone=user['phone'],
#                     is_verified=True)
#                     new_user.save()
#                     return Response({"message": "Success!"})
#                 else:
#                     return Response({"error":"Wrong code!"}, status=status.HTTP_400_BAD_REQUEST)
#             except:
#                 return Response({"error":"Wrong code!"}, status=status.HTTP_400_BAD_REQUEST)
#     print(form.errors)

#     return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["POST"])
# def edit_user(request, user_id):
#     user = User.objects.get(id=user_id)
#     user_ser = UserSerializer(data=request.data, instance=user)
#     if user_ser.is_valid():
#         user_ser.save()
#         return redirect("users")
#     return Response(user_ser.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(["DELETE"])
# def del_user(request, user_id):
#     user = User.objects.get(id=user_id)
#     user.delete()
    # return redirect("users")


# @login_required(login_url='login')
# #BranchSerializers
# @api_view(['GET'])
# def all_branch(request):
#     all_branch = Branch.objects.all()
#     br_ser = BranchSerializer(all_branch, many=True)
#     return Response(br_ser.data)

# @login_required(login_url='login')
# @api_view(['GET'])
# def one_branch(request,br_id):
#     br = Branch.objects.get(id=br_id)
#     br_ser = BranchSerializer(br,many=False)
#     return Response(br_ser.data)

# @login_required(login_url='login')
# @api_view(['POST'])
# def add_branch(request):
#     br_ser = BranchSerializer(data=request.data)
#     if br_ser.is_valid():
#         br_ser.save()
#         return redirect('api-all')


# @login_required(login_url='login')
# @api_view(['POST'])
# def edit_branch(request,br_id):
#     br = Branch.objects.get(id=br_id)
#     br_ser = BranchSerializer(data=request.data, instance=br)
#     if br_ser.is_valid():
#         br_ser.save()
#         return redirect('api-all')


# @login_required(login_url='login')
# @api_view(['DELETE'])
# def del_branch(request,br_id):
#     br = Branch.objects.get(id=br_id)
#     br.delete()
#     return Response('branch Deleted Success')


# #OfferSerializers
# @api_view(['GET'])
# def all_Offer(request):
#     all_Offer = Offer.objects.all()
#     of_ser = OfferSerializer(all_Offer, many=True)
#     return Response(of_ser.data)

# # displaying the offers of a certain branch
# @api_view(['GET'])
# def branchOffers(request, br_id):
#     branch_off = Offer.objects.filter(branch_id=br_id)
#     branch_offers = OfferSerializer(branch_off, many=True)
#     return Response(branch_offers.data)


# @api_view(['GET'])
# def one_Offer(request,of_id):
#     of = Offer.objects.get(id=of_id)
#     of_ser = OfferSerializer(of,many=False)
#     return Response(of_ser.data)

# @api_view(['POST'])
# def add_Offer(request):
#     of_ser = OfferSerializer(data=request.data)
#     if of_ser.is_valid():
#         of_ser.save()
#         return redirect('api-all')


# @api_view(['POST'])
# def edit_Offer(request,of_id):
#     of = Offer.objects.get(id=of_id)
#     of_ser = OfferSerializer(data=request.data, instance=of)
#     if of_ser.is_valid():
#         of_ser.save()
#         return redirect('api-all')

# @api_view(['DELETE'])
# def del_Offer(request,of_id):
#     of = Offer.objects.get(id=of_id)
#     of.delete()
#     return Response('Offer Deleted Success')


# #Personal Trainer Serializers
# @api_view(['GET'])
# def showBranchTrainer(request, br_id):
#     branch_pt = PersonalTrainer.objects.filter(branch_id=br_id)
#     branch_Trainers = PersonalTrainerSerializers(branch_pt, many=True)
#     return Response(branch_Trainers.data)

# @api_view(['GET'])
# def all_PersonalTrainer(request):
#     all_PersonalTrainer = PersonalTrainer.objects.all()
#     pt_ser = PersonalTrainerSerializers(all_PersonalTrainer, many=True)
#     return Response(pt_ser.data)

# @api_view(['GET'])
# def one_PersonalTrainer(request,pt_id):
#     pt = PersonalTrainer.objects.get(id=pt_id)
#     pt_ser = PersonalTrainerSerializers(pt,many=False)
#     return Response(pt_ser.data)

# @api_view(['POST'])
# def add_PersonalTrainer(request):
#     pt_ser = PersonalTrainerSerializers(data=request.data)
#     if pt_ser.is_valid():
#         pt_ser.save()
#         return redirect('api-all')


# @api_view(['POST'])
# def edit_PersonalTrainer(request,pt_id):
#     pt = PersonalTrainer.objects.get(id=pt_id)
#     pt_ser = PersonalTrainerSerializers(data=request.data, instance=pt)
#     if pt_ser.is_valid():
#         pt_ser.save()
#         return redirect('api-all')

# @api_view(['DELETE'])
# def del_PersonalTrainer(request,pt_id):
#     pt = PersonalTrainer.objects.get(id=pt_id)
#     pt.delete()
#     return Response('PersonalTrainer Deleted Success')


# # Events API
# #display all events
# @api_view(['GET'])
# def allEvents(request):
#     all_ev = Event.objects.all()
#     all_events = EventSerializer(all_ev, many=True)
#     return Response(all_events.data)


# # displaying the events of a certain branch
# @api_view(['GET'])
# def showBranchEvents(request, br_id):
#     branch_ev = Event.objects.filter(branch_id=br_id)
#     branch_events = EventSerializer(branch_ev, many=True)
#     return Response(branch_events.data)

# #adding an event to a certain branch
# @api_view(['POST'])
# def addEvent(request):
#     added_event = EventSerializer(data=request.data)
#     if added_event.is_valid():
#         added_event.save()
#         return redirect ('all-events')


# #edit event
# @api_view(['POST'])
# def editEvent(request, ev_id):
#     event = Event.objects.get(id=ev_id)
#     event_ser = EventSerializer(data=request.data, instance=event)
#     if event_ser.is_valid():
#         event_ser.save()
#         return redirect ('all-events')

# #delete event
# @api_view(['DELETE'])
# def delEvent(request,ev_id):
#     event = Event.objects.get(id=ev_id)
#     event.delete()
#     return HttpResponse ('Event deleted')

# #add event form for testing
# def addingEvent(request):
#     if request.method == 'POST':
#         form = EventForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('all-events')
#     else:
#         form = EventForm()
#         return render(request, 'physio-slim/addeventform.html', {'form' : form})


# # Classes API
# #display all classes
# @api_view(['GET'])
# def allClasses(request):
#     all_cl = Class.objects.all()
#     all_classes = ClassSerializer(all_cl, many=True)
#     return Response(all_classes.data)


# # displaying the events of a certain branch
# @api_view(['GET'])
# def showBranchClasses(request, br_id):
#     branch_cl = Class.objects.filter(branch_id=br_id)
#     branch_classes = ClassSerializer(branch_cl, many=True)
#     return Response(branch_classes.data)

# #adding an event to a certain branch
# @api_view(['POST'])
# def addClass(request):
#     added_class = ClassSerializer(data=request.data)
#     if added_class.is_valid():
#         added_class.save()
#         return redirect ('all-classes')


# #edit event
# @api_view(['POST'])
# def editClass(request, cl_id):
#     classes = Class.objects.get(id=cl_id)
#     classes_ser = ClassSerializer(data=request.data, instance=classes)
#     if classes_ser.is_valid():
#         classes_ser.save()
#         return redirect ('all-classes')

# #delete event
# @api_view(['DELETE'])
# def delClass(request,ev_id):
#     event = Class.objects.get(id=ev_id)
#     event.delete()
#     return HttpResponse ('Class deleted')


# #add clinic form for testing
# # def addingClinic(request):
# #     if request.method == 'POST':
# #         form = ClinicForm(request.POST, request.FILES)
# #         if form.is_valid():
# #             form.save()
# #             return redirect('all-events')
# #     else:
# #         form = ClinicForm()
# #         return render(request, 'physio-slim/addClinicForm.html', {'form' : form})


# # Clinics API
# #display all clinics
# @api_view(['GET'])
# def allClinics(request):
#     all_cl = Clinic.objects.all()
#     all_clinics = ClinicSerializer(all_cl, many=True)
#     return Response(all_clinics.data)


# # displaying the clinics of a certain branch
# @api_view(['GET'])
# def showBranchClinics(request, br_id):
#     branch_cl = Clinic.objects.filter(branch_id=br_id)
#     branch_clinics = ClinicSerializer(branch_cl, many=True)
#     return Response(branch_clinics.data)

# #adding a clinic to a certain branch
# @api_view(['POST'])
# def addClinic(request):
#     added_clinic= ClinicSerializer(data=request.data)
#     if added_clinic.is_valid():
#         added_clinic.save()
#         return redirect ('all-clinics')


# add event form for testing
def addingEvent(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all-events')
    else:
        form = EventForm()
        return render(request, 'physio-slim/addeventform.html', {'form': form})
