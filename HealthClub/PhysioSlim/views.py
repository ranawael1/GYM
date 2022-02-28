<<<<<<< HEAD
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

=======
from django.shortcuts import redirect, render
from .models import User
from .forms import CreateUserForm
#rest_framework imports
from rest_framework.response import Response # like render
from rest_framework.decorators import api_view
from .serializers import UserSerializer


@api_view(['GET'])
def api_users(request):
    users = User.objects.all()
    users_ser = UserSerializer(users, many=True)
    return Response(users_ser.data)


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST, request.FILES)
        print("before")
        if form.is_valid():
            print("valid")
            user = form.save(commit=False)
            user.save()
            return redirect('api-users')
    context = {'form':form}
    return render(request, 'physio-slim/register.html', context)

>>>>>>> f457ee587af00c656df43e41c70279c6f78e2d98
