from enum import Flag
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.http import HttpResponse

#if the user is logged in they will be directed to their home page
#a decorater to be used above the function if needed
def unauthenticated_user(view_func):
    def wrapper_func(request, *args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args,**kwargs)
    return wrapper_func

def unverified_user(view_func):
    def wrapper_func(request, *args,**kwargs):
        if request.user.is_authenticated:
            if request.user.is_verified == False:
                return redirect('verify-code')
            else:     
                return view_func(request, *args,**kwargs)
        else:     
            return view_func(request, *args,**kwargs)
    return wrapper_func

def verification_required(view_func):
    def wrapper_func(request, *args,**kwargs):
        if not request.user.is_verified:
            return redirect('verify-code')
        else:
            return view_func(request, *args,**kwargs)
    return wrapper_func
    