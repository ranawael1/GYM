from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('home/',views.home, name='home'),
    #verify phone
    path('verify/', views.verify_code, name='verify-code'),  
    path('re-verify/', views.reverify_code, name='re-verify'),  

    #reset password form
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset/password_reset.html"), name="reset_password"),
    #notify the user to check their email 
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset/password_reset_sent.html"), name="password_reset_done"),
    #sending user id encoded and making sure the password is valid
    path('reset_password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset/password_reset_form.html"), name='password_reset_confirm'),
    #success
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'), name="password_reset_complete"),
    #notifications
    # path('test/', views.test, name="test"),

    # access branch
    path('branch/<br_id>', views.branch, name='branch'),
    # access classes
    path('class/<br_id>', views.classe, name='class'),
    # access clinics
    path('clinics/<br_id>', views.clinics, name='clinics'),

    #notification
    path('ClassNotifications/<notification_id>/<Class_id>', views.ClassNotifications, name='ClassNotifications'),
    path('EventNotifications/<notification_id>/<Event_id>', views.EventNotifications, name='EventNotifications'),
    path('RemoveNotifications/<notification_id>', views.RemoveNotifications, name='RemoveNotifications'),
    path('FollowNotifications/<notification_id>/<follow_id>', views.FollowNotifications, name='FollowNotifications'),
    # access offers
    path('offers/<br_id>', views.offers, name='offers'),
    # access PersonalTrainers
    path('PersonalTrainers/<br_id>', views.PersonalTrainers, name='PersonalTrainers'),
    #subscribetoclass
    path('subscribe-to-class/<class_id>', views.subscribeToClass, name='subscribe-to-class'),
    path('unsubscribe-from-class/<class_id>', views.unSubscribeFromClass, name='unsubscribe-from-class'),

    # #rest_framework
    # path('users/', views.users, name='users'),
    # path('user/<user_id>', views.user, name='user'),
    # path('add-user/', views.add_user, name='add-user'),
    # path('login/',views.login_view,name='login'),
    # # path('verify/', views.verify_code, name='verify-code'),
    # # path('verify/', views.verify_code, name='verify-code'),
    # path('api-verify/', views.verify_code_api, name='verify-code-api'),
    # path('edit-user/<user_id>', views.edit_user, name='edit-user'),
    # path('delete-user/<user_id>', views.del_user, name='delete-user'),

    # #api-branch
    # path('branch-all/', views.all_branch, name='branch-all'),
    # path('branch/<br_id>', views.one_branch, name='branch'),
    # path('branch-add', views.add_branch, name='branch-add'),
    # path('branch-edit/<br_id>', views.edit_branch, name='branch-edit'),
    # path('branch-del/<br_id>', views.del_branch, name='branch-del'),
    # #api-Offer
    # path('Offer-all/', views.all_Offer, name='Offer-all'),
    # path('branch-offers/<br_id>', views.branchOffers, name='branch-offers'),
    # path('Offer-one/<of_id>', views.one_Offer, name='Offer-one'),
    # path('Offer-add', views.add_Offer, name='Offer-add'),
    # path('Offer-edit/<of_id>', views.edit_Offer, name='Offer-edit'),
    # path('Offer-del/<of_id>', views.del_Offer, name='Offer-del'),
    # #api-PersonalTrainer
    # path('PersonalTrainer-all', views.all_PersonalTrainer, name='PersonalTrainer-all'),
    # path('branch-trainers/<br_id>', views.showBranchTrainer, name='branch-trainers'),
    # path('PersonalTrainer-one/<pt_id>', views.one_PersonalTrainer, name='PersonalTrainer-one'),
    # path('PersonalTrainer-add', views.add_PersonalTrainer, name='PersonalTrainer-add'),
    # path('PersonalTrainer-edit/<pt_id>', views.edit_PersonalTrainer, name='PersonalTrainer-edit'),
    # path('PersonalTrainer-del/<pt_id>', views.del_PersonalTrainer, name='PersonalTrainer-del'),
    # #api-event
    # path('all-events/', views.allEvents, name='all-events'),
    # path('branch-events/<br_id>', views.showBranchEvents, name='branch-events'),
    # path('add-event/', views.addEvent, name='add-event'),
    # path('edit-event/<ev_id>', views.editEvent, name='edit-event'),
    # path('del-event/<ev_id>', views.delEvent, name='del-event'),
    # #api-Class
    # path('all-classes/', views.allClasses, name='all-classes'),
    # path('branch-classes/<br_id>', views.showBranchClasses, name='branch-classes'),
    # path('add-class/', views.addClass, name='add-class'),
    # path('edit-class/<ev_id>', views.editClass, name='edit-class'),
    # path('del-class/<ev_id>', views.delClass, name='del-class'),

    # #api-event
    # path('all-clinics/', views.allClinics, name='all-clinics'),
    # path('branch-clinics/<br_id>', views.showBranchClinics, name='branch-clinics'),
    # path('add-clinic/', views.addClinic, name='add-clinic'),
    # path('edit-clinic/<cl_id>', views.editClinic, name='edit-clinic'),
    # path('del-clinic/<cl_id>', views.delClinic, name='del-clinic'),

    #add-event-form
    # path('add-event-form/', views.addingEvent, name='add-event-form'),
    #add-clinic-form
    # path('add-clinic-form/', views.addingClinic, name='add-clinic-form'),
  
    # #add-event-form
    # path('add-event-form/', views.addingEvent, name='add-event-form'),
    # #add-clinic-form
    # # path('add-clinic-form/', views.addingClinic, name='add-clinic-form'),
]
