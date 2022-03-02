from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_2, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    #reset password form
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset/password_reset.html"), name="reset_password"),
    #notify the user to check their email 
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset/password_reset_sent.html"), name="password_reset_done"),
    #sending user id encoded and making sure the password is valid
    path('reset_password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset/password_reset_form.html"), name='password_reset_confirm'),
    #success
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'), name="password_reset_complete"),

    #rest_framework
    path('users/', views.users, name='users'),
    path('user/<user_id>', views.user, name='user'),
    path('add-user/', views.add_user, name='add-user'),
    # path('verify/', views.verify_code, name='verify-code'),  
    #api-branch  
    path('branch-all/', views.all_branch, name='branch-all'),
    path('branch-one/<br_id>', views.one_branch, name='branch-one'),
    path('branch-add', views.add_branch, name='branch-add'),
    path('branch-edit/<br_id>', views.edit_branch, name='branch-edit'),
    path('branch-del/<br_id>', views.del_branch, name='branch-del'),
    #api-Offer  
    path('Offer-all/', views.all_Offer, name='Offer-all'),
    path('Offer-one/<of_id>', views.one_Offer, name='Offer-one'),
    path('Offer-add', views.add_Offer, name='Offer-add'),
    path('Offer-edit/<of_id>', views.edit_Offer, name='Offer-edit'),
    path('Offer-del/<of_id>', views.del_Offer, name='Offer-del'),
    #api-event  
    path('all-events/', views.allEvents, name='all-events'),
    path('branch-events/<br_id>', views.showBranchEvents, name='branch-events'),
    path('add-event/', views.addEvent, name='add-event'),
    path('edit-event/<ev_id>', views.editEvent, name='edit-event'),
    path('del-event/<ev_id>', views.delEvent, name='del-event'),
    #add-event-form
    path('add-event-form/', views.addingEvent, name='add-event-form'),
]

