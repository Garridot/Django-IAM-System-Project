from django.urls import path
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import *

urlpatterns = [   
    path('registration/', CustomRegistrationView.as_view(), name='registration'),   
    path('login/', CustomLoginView.as_view(), name='login'), 
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password_update/', CustomPasswordUpdateView.as_view(), name='password_update'), 
    path('reset-password/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name = 'accounts/password_reset/password_reset_done.html'), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name = 'accounts/password_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset-password/complete/', PasswordResetCompleteView.as_view(template_name = 'accounts/password_reset/password_reset_complete.html'), name='password_reset_complete'),
    path('profile/delete/', ProfileDeleteView.as_view(), name='profile_delete'),
]

