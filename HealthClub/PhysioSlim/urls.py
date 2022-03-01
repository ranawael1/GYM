from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_2, name='login'),

    #rest_framework
    path('users/', views.users, name='users'),
    path('user/<user_id>', views.user, name='user'),
    path('add-user/', views.add_user, name='add-user'),
    path('verify/', views.verify_code, name='verify-code'),  
    #api-branch  
    path('branch-all', views.all_branch, name='branch-all'),
    path('branch-one/<br_id>', views.one_branch, name='branch-one'),
    path('branch-add', views.add_branch, name='branch-add'),
    path('branch-edit/<br_id>', views.edit_branch, name='branch-edit'),
    path('branch-del/<br_id>', views.del_branch, name='branch-del'),
    #api-Offer  
    path('Offer-all', views.all_Offer, name='Offer-all'),
    path('Offer-one/<of_id>', views.one_Offer, name='Offer-one'),
    path('Offer-add', views.add_Offer, name='Offer-add'),
    path('Offer-edit/<of_id>', views.edit_Offer, name='Offer-edit'),
    path('Offer-del/<of_id>', views.del_Offer, name='Offer-del'),
    
]

