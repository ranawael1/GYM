from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logoutuser, name='logout'),

    #rest_framework
    path('users/', views.users, name='users'),
    path('user/<user_id>', views.user, name='user'),
    #path('add-user/', views.add_user, name='add-user'),
    # path('verify/', views.verify_code, name='verify-code'),
    #api-branch  
    path('api-all', views.api_all_branch, name='api-all'),
    path('api-one/<br_id>', views.api_one_branch, name='api-one'),
    path('api-add', views.api_add_branch, name='api-add'),
    path('api-edit/<br_id>', views.api_edit_branch, name='api-edit'),
    path('api-del/<br_id>', views.api_del_branch, name='api-del'),
]

