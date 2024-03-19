"""
ASGI config for iam_system_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iam_system_project.settings')

# application = get_asgi_application()

"""
I. Importing Libraries:

The import os statement imports the os module, which provides a way to interact with the operating system.
The updated line (from django.core.asgi import get_asgi_application) imports the get_asgi_application function from the django.core.asgi module. This function returns the ASGI application object for your Django project.
II. Setting the Django Settings Module:

The line os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings') sets the environment variable DJANGO_SETTINGS_MODULE to specify the location of your Django project's settings.
In this example, it is set to 'myproject.settings', assuming your project's settings module is located in the myproject directory.
III. Defining the application Variable:

The application variable is a key component in the ASGI (Asynchronous Server Gateway Interface) setup.
The ProtocolTypeRouter class from the channels.routing module is used to define a dictionary-based protocol router that routes different protocols to appropriate applications.
In this case, the router is defined with two keys:

"http": The HTTP protocol is routed to the get_asgi_application() function, which returns the ASGI application object for handling HTTP requests.
"websocket": The WebSocket protocol is routed to the AllowedHostsOriginValidator, which is used for validating the origin of incoming WebSocket connections. It wraps the URLRouter and allows connections from allowed hosts.
The URLRouter is initialized with websocket_urlpatterns imported from the myapp.routing module. This variable contains the URL patterns for WebSocket connections in your application.
These changes are made in the asgi.py file of your Django project and help configure the ASGI application to handle HTTP requests and WebSocket connections using Django Channels.
"""


import os
from chat.routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iam_system_project.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        'http': django_asgi_app,
        'websocket': AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(websocket_urlpatterns))),
    }
)
