# from django.contrib.auth import get_user_model
# from django.contrib.auth import ModelBackend

from PhysioSlim.models import User

class EmailBackend():
    """
    Custom Email Backend to perform authentication via email
    """
    def authenticate(self, request ,username, password):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password): # check valid password
                return user # return user to be authenticated
        except User.DoesNotExist: # no matching user exists 
            return None 

    def get_user(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None