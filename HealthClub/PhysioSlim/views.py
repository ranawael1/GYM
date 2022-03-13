from django.shortcuts import redirect, render
from .models import Working_days, Schedule, User,Working_days, Branch, Offer, Event, Class, Clinic, PersonalTrainer,ClassSubscribers, Notifications,Gallery,MainOffer,EventParticipants,Schedule
# decorators and authentication
from .decorators import authenticated_user, verified_user, unverified_user, google_activated, google_unactivated
# forms
from .forms import  CreateUserForm, EditUserForm, VerifyForm, activateAccount
# authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# send email
from django.core.mail import send_mail
# verify phone 
from . import verify
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer

# rest framework
# from .decorators import verification_required
# from rest_framework import permissions
# from rest_framework.views import exception_handler
# from rest_framework import status
# from django.contrib.auth.hashers import make_password
# from django.contrib.auth.models import AnonymousUser
# from urllib.parse import urlparse
# from urllib import parse
#from django.http import HttpResponse
# import json

# Notifications
# from channels.layers import get_channel_layer #broadcast (not used)
#from asgiref.sync import async_to_sync


#Register
@authenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)   
            phone = form.cleaned_data.get('phone')
            # verification phone
            try:
                verify.send(phone)
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('verify-code')
            except:
                error = {
                    "error": {
                        "statusCode": 429,
                        "message": "Rate limit is exceeded. Try again later"
                    }
                }
                context = {'form': form}
                return render(request, 'physio-slim/register.html', context)
        else:
            # print(form.errors)
            context = {'form': form}
            return render(request, 'physio-slim/register.html', context)
    context = {'form': form}
    return render(request, 'physio-slim/register.html', context)

#Verify Register
@verified_user
@login_required(login_url='login')
def verify_code(request):
    if request.method == 'POST':
        user = request.user
        form = VerifyForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            code = form.cleaned_data.get('code')
            phone = user.phone
            # check verification of phone
            try:
                x = verify.check(phone, code)
                if x is not False:
                    user.is_verified = True
                    user.save()
                    return redirect('home')
                else:
                    context={ 'error': 'Wrong code'}
                    return render(request, 'physio-slim/verify.html', context)
            except:
                return render(request, 'physio-slim/verify.html', context)
        context = {'form': form}
        return render(request, 'physio-slim/verify.html', context)
    else:
        form = VerifyForm()
        context = {'form': form}
        return render(request, 'physio-slim/verify.html', context)

# reverify Register
@verified_user
@login_required(login_url='login')
def reverify_code(request):
    verify.send(request.user.phone)
    form = VerifyForm()
    context = {'form': form}
    return render(request, 'physio-slim/verify.html', context)

# activate google account
@google_activated
@login_required(login_url='login')
def activate(request):
    notifications = UserNotifications(request)
    branches = Branch.objects.all()
    user = User.objects.get(id=request.user.id)
    form = activateAccount(instance=user)
    if request.method == 'POST':
        form = activateAccount(request.POST ,request.FILES ,instance = user)
        if form.is_valid():
            user = form.save(commit=False)   
            phone = form.cleaned_data.get('phone')
            # verification phone
            # print(phone)
            try:
                verify.send(phone)
                user.save()
                # print("suser")
                return redirect('verify-code')
            except:
                error = {
                    "error": {
                        "statusCode": 429,
                        "message": "Rate limit is exceeded. Try again later"
                    }
                }
            context = {'form':form,'branches':branches,'notifications':notifications}
            return render(request, 'physio-slim/activate.html', context)
        # print(form.errors)
    context = {'form':form,'branches':branches,'notifications':notifications}
    return render(request,'physio-slim/activate.html', context)

# login
@authenticated_user
def loginUser(request):
    if request.method == 'POST':
        # gather the username and the password entered on the login form
        username = request.POST.get('username')
        password = request.POST.get('password')
        # authenticate the data entered by the user
        user = authenticate(request, username=username, password=password)
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

# Logout
@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    # return redirect(request.META.get('HTTP_REFERER'))  #to stay in the same page after logging out
    return redirect('home')

# Home
def home(request):
    gallery = Gallery.objects.all()[0:4]
    offers= MainOffer.objects.all()[0:4]
    branches = Branch.objects.all()[0:4]
    events = Event.objects.all()[0:3]
    if not request.user.is_anonymous : 
        notifications = UserNotifications(request)
        context = {'gallery' : gallery ,'offers':offers,'events':events ,'notifications' : notifications, 'branches' : branches }
    else: 
        context = {'gallery' : gallery , 'offers':offers ,'events':events,'branches':branches}
    return render(request,'physio-slim/index.html', context)
   
#Gallery Page
def gallery(request):
    gallery = Gallery.objects.all()
    if not request.user.is_anonymous : 
        notifications = UserNotifications(request)
        context = {'gallery' : gallery , 'notifications' : notifications }
    else: 
        context = {'gallery' : gallery }
    return render(request,'physio-slim/gallery.html', context)

#Main offers Page
def main_offers(request):
    offers = MainOffer.objects.all()
    if not request.user.is_anonymous : 
        notifications = UserNotifications(request)
        context = {'offers': offers, 'notifications' : notifications }
    else: 
        context = {'offers': offers }
    return render(request, 'physio-slim/m_offers.html', context)

# Event Page 
def events(request):
    branches=Branch.objects.all()
    events = Event.objects.all()
    if not request.user.is_anonymous : 
        notifications = UserNotifications(request)
        context = { 'events': events , 'notifications':notifications,'branches':branches}
    else:
        context = {'events':events, 'branches':branches}
    return render(request, 'physio-slim/events.html', context)


#going to an event
def goingtToEvent(request, event_id):
    event = Event.objects.get(id=event_id)
    participant = EventParticipants.objects.create(participant=request.user, event=event)
    return redirect ('event',event_id)

#not going to an event
def notGoingtToEvent(request, event_id):
    event = Event.objects.get(id=event_id)
    event_praticipant = EventParticipants.objects.get(participant=request.user, event_id=event)
    event_praticipant.delete()
    return redirect ('event',event_id)
#Contact Page
def contact(request):
    branches = Branch.objects.all()
    if not request.user.is_anonymous : 
        notifications = UserNotifications(request)
        context = { 'branches' : branches , 'notifications' : notifications }
    else: 
        context = { 'branches' : branches }
    return render(request,'physio-slim/contact.html', context)

#About Page
def about(request):
    branches = Branch.objects.all()
    if not request.user.is_anonymous : 
        notifications = UserNotifications(request)
        context = {'branches': branches , 'notifications' : notifications }
    else:
        context = { 'branches': branches }
    return render(request,'physio-slim/about.html', context)

# User page
@google_unactivated
@login_required(login_url='login')
def profile(request):
    notifications = UserNotifications(request)
    branches = Branch.objects.all()
    user = User.objects.get(id=request.user.id)
    form = EditUserForm(instance=user)
    if request.method == 'POST':
        form = EditUserForm(request.POST ,request.FILES ,instance = user)
        # print('valid or not')
        if form.is_valid():
            edit = form.save(request, commit=False)
            # print('valid')
            phone = form.cleaned_data.get('phone')
            # print('is verified')
            if not edit.is_verified:
                edit.save()
                return redirect("verify-code")    
            else:
                edit.save()
                return redirect("home")
        # print(form.errors)
    context = {'form':form,'branches':branches,'notifications':notifications}
    return render(request,'physio-slim/profile.html', context)

# Branch Page
def branch(request, br_id):
    branches = Branch.objects.all()
    branch = Branch.objects.get(id=br_id)
    classes = Class.objects.filter(branch=br_id)[0:3]
    clinics = Clinic.objects.filter(branch=br_id)[0:3]
    offers = Offer.objects.filter(branch=br_id)[0:4]
    trainers = PersonalTrainer.objects.filter(branch=br_id)[0:3]
    if not request.user.is_anonymous : 
        notifications = UserNotifications(request)
        context = {'branch': branch, 'classes': classes,
               'clinics': clinics, 'offers': offers, 'trainers': trainers, 'notifications' : notifications, 'branches':branches}
    else :
        context = {'branch': branch, 'classes': classes,
               'clinics': clinics, 'offers': offers, 'trainers': trainers, 'branches':branches}
    return render(request, 'physio-slim/branch.html', context)

#Classes Branch page
def classes(request, br_id):
    branches = Branch.objects.all()
    branch = Branch.objects.get(id=br_id)
    classes = Class.objects.filter(branch=br_id)
    notifications = UserNotifications(request)
    if not request.user.is_anonymous:
        all_subscribers = ClassSubscribers.objects.filter(subscriber=request.user).values_list('favclass_id', flat=True)
        context = {'classes': classes, 'branch': branch,
                'branches': branches, 'all_subscribers':all_subscribers, 'notifications' : notifications  }
    else:
        context = {'classes': classes, 'branch': branch,
                'branches': branches }
    return render(request, 'physio-slim/classes.html', context)

# # schedule of class
def class_scheduale(request,cl_id ):
    branches = Branch.objects.all()
    days= Working_days.objects.all()
    classes= Class.objects.get(id=cl_id)
    classs = Schedule.objects.filter(classes=cl_id)
    context= {'branches':branches ,'days':days, 'classes':classes , 'class':classs}
    return render(request, 'physio-slim/schedule.html',context )

# subscribe to a Class
@google_unactivated
@unverified_user
@login_required(login_url='login')
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
    # send email to the management to contact the subscriber
    send_mail(
        'New user subscribed!',
        f'The user: {request.user} \n has subscribed to: {classs} class, \n branch: {request.user.branch}, \n phone number:{request.user.phone} ',
        'physio.slim2@gmail.com',
        ['physio.slim2@gmail.com'],
        fail_silently=False,)
        # send email confirming subscription
    # send_mail(
    #     'Subscription Successful!',
    #     f'Hello {request.user} Thank you for subscribing to our {classs} class, welcome on board \n you might receive a call from our side to have a further discussion', 
    #     'physio.slim2@gmail.com',
    #     [f'{email}'],
    #     fail_silently=False,)
    return redirect('classes', branch)

#display favorite classes
@google_unactivated
@unverified_user
@login_required(login_url='login')
def favoriteClasses(request):
    notifications = UserNotifications(request)
    branches = Branch.objects.all()
    all_subscribers = ClassSubscribers.objects.filter(subscriber=request.user).values_list('favclass_id', flat=True)
    #getting the classes the user subscribed to
    favorite_classes = ClassSubscribers.objects.filter(subscriber_id=request.user.id).values_list('favclass_id', flat=True)
    #turning it into a list
    fav_classes=list(favorite_classes)
    #getting the info of the favorite classes from the Class Model
    classes = Class.objects.filter(id__in = fav_classes)
    context={'classes':classes, 'all_subscribers':all_subscribers,'notifications':notifications, 'branches':branches}
    return render(request, 'physio-slim/favorites.html', context)

# Unsubscribe from a class
@google_unactivated
@unverified_user
@login_required(login_url='login')
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
    send_mail(
        'User unsubscribed!',
        f'The user: {request.user} \n unsubscribed from: {classs} class, \n branch: {request.user.branch}, \n phone number:{request.user.phone} ',
        'physio.slim2@gmail.com',
        ['physio.slim2@gmail.com'],
        fail_silently=False,)
        # send email confirming the unsubscription
    # send_mail(
    #     'Unsubscription',
    #     f'Hello {request.user},\n sorry to here that you unsubscribed from our {classs} class, \n you might receive a call from our side to have a further discussion \n Br, \n Physio-Slim management.', 
    #     'physio.slim2@gmail.com',
    #     [f'{email}'],
    #     fail_silently=False,)
    return redirect('classes', branch)

# !!!!!!!!!!!!!!!! Notifications!!!!!!!!!!!!!!!!!
# clinics Branch page
def clinics(request, br_id):
    branch = Branch.objects.get(id=br_id)
    clinic = Clinic.objects.filter(branch=br_id)
    context = {'clinics': clinic, 'branch': branch}
    return render(request, 'physio-slim/br_clinics.html', context)

# !!!!!!!!!!!!!!!! Notifications!!!!!!!!!!!!!!!!!

# Event Detailes Page
def event_details(request, ev_id):
    branches=Branch.objects.all()
    event= Event.objects.filter(id = ev_id)
    #using this flag in case the event doesn't have a limited participants then no need to show 'going to' option
    hide_going_to_option = False
    #try, because if the event doesnt have a limited number, then it will give an error
    try:
        going_to = False 
        #original available places
        original_num_of_participants = list(Event.objects.filter(id=ev_id).values_list('num_of_participants', flat=True))[0]
        #getting the participants IDs to this event so far
        this_event_participants = EventParticipants.objects.filter(event_id=ev_id).values_list('participant_id', flat=True)
        #turn it into a list so we can get its length (number of participants)
        this_event_participants_list = list(this_event_participants)
        #available places
        available_places = original_num_of_participants - len(this_event_participants_list) 
        #change the going_to flag to True if the user was found in the (this_event_participants_list)
        #going_to flag will be used to give the user the option to undo the 'going to' option
        if request.user.id in this_event_participants_list:
            going_to = True
        context = { 
                    'event': event, 
                    'branch': branch , 
                    'branches':branches,
                    'hide_going_to_option':hide_going_to_option, 
                    'going_to':going_to,
                    'available_places':available_places,
                    'this_event_participants':this_event_participants,
                }
    except:
        hide_going_to_option = True
        context = {
                    'event': event, 
                    'branch': branch ,
                    'branches':branches,
                    'hide_going_to_option':hide_going_to_option,
                }
    return render(request, 'physio-slim/event.html', context)

# offers Branch page
def offers(request, br_id):
    branches=Branch.objects.all()
    branch = Branch.objects.get(id=br_id)
    offers = Offer.objects.filter(branch=br_id)
    if not request.user.is_anonymous : 
        notifications = UserNotifications(request)
        context = {'offers': offers, 'branch': branch, 'notifications':notifications,'branches':branches}
    else:
        context = {'offers': offers, 'branch': branch, 'branches':branches}
    return render(request, 'physio-slim/offers.html', context)

#Trainers Branch page
def trainers(request, br_id):
    branch = Branch.objects.get(id=br_id)
    branches=Branch.objects.all()
    trainers = PersonalTrainer.objects.filter(branch=br_id)
    if not request.user.is_anonymous : 
        notifications = UserNotifications(request)
        context = {'trainers': trainers, 'branch': branch, 'notifications' : notifications, 'branches':branches }
    else: 
        context = {'trainers': trainers, 'branch': branch, 'branches':branches }
    return render(request, 'physio-slim/trainers.html', context)

# Showing notifications (function not url)
def UserNotifications(request):
    notification = Notifications.objects.filter(to_user = request.user)
    notification.user_seen = True
    return notification

# Redirect to notifications
@google_unactivated
@unverified_user
@login_required(login_url='login')
def ClassNotifications(request,notification_id,class_id):
    notification = Notifications.objects.get(id = notification_id)
    classs = Class.objects.get(id=class_id)
    branch = request.user.branch_id
    notification.user_seen = True
    notification.save()
    return redirect('classes',branch)

@google_unactivated
@unverified_user
@login_required(login_url='login')
def EventNotifications(request,notification_id,event_id):
    notification = Notifications.objects.get(id = notification_id)
    event = Event.objects.get(id = event_id)
    notification.user_seen = True
    notification.save()
    return redirect('home')

@google_unactivated
@unverified_user
@login_required(login_url='login')
def TrainerNotifications(request,notification_id,trainer_id,branch_id):
    notification = Notifications.objects.get(id = notification_id)
    trainer = PersonalTrainer.objects.get(id = trainer_id)
    branch = Branch.objects.get(id = branch_id)
    notification.user_seen = True
    notification.save()
    return redirect('branch',br_id=branch_id)

@google_unactivated
@unverified_user
@login_required(login_url='login')
def OfferNotifications(request,notification_id,offer_id,branch_id):
    notification = Notifications.objects.get(id = notification_id)
    offer = Offer.objects.get(id = offer_id)
    branch = Branch.objects.get(id = branch_id)
    notification.user_seen = True
    notification.save()
    return redirect('branch',br_id=branch_id)

@google_unactivated
@unverified_user
@login_required(login_url='login')
def MOfferNotifications(request,notification_id,offer_id):
    notification = Notifications.objects.get(id = notification_id)
    offer = MainOffer.objects.get(id = offer_id)
    notification.user_seen = True
    notification.save()
    return redirect('main-offers')

#Removing Notification
@google_unactivated
@unverified_user
@login_required(login_url='login')
def RemoveNotifications(request, notification_id):
    notification = Notifications.objects.get(id = notification_id)  
    # notification.user_seen = True
    notification.to_user.remove(request.user)
    notification.save()
    return redirect('home')
  


#class Subscirbers API
@api_view(['GET',])
def classSubscribers(request, class_id):
    subscribers_id = list(ClassSubscribers.objects.filter(favclass_id=class_id).values_list('subscriber_id', flat=True))
    subscribers_data = User.objects.filter(id__in = subscribers_id)
    subscribers_ser = UserSerializer(subscribers_data, many=True)
    return Response(subscribers_ser.data)




# def showNotifications(request):
#     notification = Notifications.objects.filter(to_user = request.user)
#     context = {'notifications': notifications}
#     return render(request, 'physio-slim/index.html', context)



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
# def addingEvent(request):
#     if request.method == 'POST':
#         form = EventForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('all-events')
#     else:
#         form = EventForm()
#         return render(request, 'physio-slim/addeventform.html', {'form': form})
