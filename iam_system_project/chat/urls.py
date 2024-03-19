from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatroomsView.as_view(), name='index')
]