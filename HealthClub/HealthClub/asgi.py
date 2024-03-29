# """
# ASGI config for HealthClub project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
# """
# import os
# import django
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HealthClub.settings')
# django.setup()

# from channels.auth import AuthMiddleware, AuthMiddlewareStack
# from notifications_app.routing import websocket_urlpatterns
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     )
# })

# #AuthMiddlewareStack is used to check which function in consumer requested for 

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HealthClub.settings')

application = get_asgi_application()
