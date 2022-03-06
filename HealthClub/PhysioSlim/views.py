import email
import imp
from multiprocessing import context
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
#rest_framework imports
from rest_framework.response import Response # like render
from rest_framework.decorators import api_view
from .serializers import ClinicSerializer, UserSerializer,BranchSerializer,OfferSerializer,EventSerializer,VerifySerializer,PersonalTrainerSerializers,ClassSerializer
from .serializers import UserSerializer,BranchSerializer,OfferSerializer,EventSerializer,VerifySerializer,PersonalTrainerSerializers,ClassSerializer,LoginSerializer
from . import verify
#from rest_framework import permissions
# from rest_framework.views import exception_handler
# from rest_framework import status


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
#                 return redirect('home')
#     else:
#         form = VerifyForm()
#         context = {'form': form}
#     return render(request, 'physio-slim/verify.html', context)


def verify_code(request, user):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            code = form.cleaned_data.get('code')
            phone = user.phone
            try:
                x=verify.check(user.phone, code)
                if x is not False:
                    user.save()
                    return redirect('users')
                else:
                    return render(request, 'physio-slim/verify.html', context)
            except:
                return render(request, 'physio-slim/verify.html', context)
        context = {'form': form}
        return render(request, 'physio-slim/verify.html', context)
    else:
        form = VerifyForm()
        context = {'form': form}
        return render(request, 'physio-slim/verify.html', context)



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


#logout
def logoutUser(request):
    logout(request)
    # return redirect(request.META.get('HTTP_REFERER'))  #to stay in the same page after logging out
    return redirect('home')

#home
def home(request):
    branches = Branch.objects.all()
    context={'branches':branches}
    return render(request, 'physio-slim/home.html', context)
# branch  details
def branch(request, br_id):
    branches = Branch.objects.all()
    branch = Branch.objects.get(id = br_id)
    classe= Class.objects.filter(branch= br_id )[0:3]
    # print(classe)
    clinic= Clinic.objects.filter(branch=br_id)
    events=Event.objects.filter(branch=br_id)
    print(events)
    context ={'branch':branch, 'classes':classe ,'events':events,'clinics':clinic,'branches':branches}
    return render(request,'physio-slim/branchHomePage.html', context)

def classe(request,br_id):
    branches = Branch.objects.all()
    branch = Branch.objects.get(id = br_id)
    classe= Class.objects.filter(branch= br_id )
    print(classe)
    context= {'classes':classe ,'branch':branch, 'branches':branches }
    return render(request,'physio-slim/br_class.html', context)

def clinics(request,br_id):
    branch = Branch.objects.get(id = br_id)
    clinic= Clinic.objects.filter(branch= br_id )
    print(clinic)
    context= {'clinics':clinic,'branch':branch }
    return render(request,'physio-slim/br_clinics.html', context)


    


    


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


# #edit clinic
# @api_view(['POST'])
# def editClinic(request, cl_id):
#     clinic = Clinic.objects.get(id=cl_id)
#     clinic_ser = ClinicSerializer(data=request.data, instance=clinic)
#     if clinic_ser.is_valid():
#         clinic_ser.save()
#         return redirect ('all-clinics')

# #delete clinic
# @api_view(['DELETE'])
# def delClinic(request,cl_id):
#     clinic = Clinic.objects.get(id=cl_id)
#     clinic.delete()
#     return HttpResponse ('Clinic deleted')