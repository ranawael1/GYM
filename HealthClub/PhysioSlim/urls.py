from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login', views.login_2, name='login'),

    #rest_framework
    path('users/', views.users, name='users'),
    path('user/<user_id>', views.user, name='user'),
    #path('add-user/', views.add_user, name='add-user'),
    path('verify/', views.verify_code, name='verify-code'),  
]

