from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect




def verification_required(view_func):
    def wrapper_func(request, *args,**kwargs):
        if not request.user.is_verified:
            return redirect('verify-code')
        else:
            return view_func(request, *args,**kwargs)
    return wrapper_func
    