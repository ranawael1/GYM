from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login', views.login_2, name='login'),

    #rest_framework
    path('api-users/', views.api_users, name='api-users'),
    # path('api-user/<user_id>', views.api_user, name='api-user'),
]

