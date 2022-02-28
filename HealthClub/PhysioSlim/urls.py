<<<<<<< HEAD
=======
   
>>>>>>> f457ee587af00c656df43e41c70279c6f78e2d98
from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD

    path('all', views.all, name='api-all'),

]
=======
    path('register/', views.register, name='register'),

    #rest_framework
    path('api-users/', views.api_users, name='api-users'),
    # path('api-user/<user_id>', views.api_user, name='api-user'),
]

>>>>>>> f457ee587af00c656df43e41c70279c6f78e2d98
