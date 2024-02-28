from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView 
from django.contrib.auth import login, authenticate
from django.contrib import messages

from django.http import HttpResponseRedirect

from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy

from .forms import *

from django.contrib.auth import logout

from django.http import HttpResponseForbidden
from functools import wraps

def user_not_authenticated(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseForbidden("You are already logged in.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@method_decorator(user_not_authenticated, name='dispatch')
class CustomRegistrationView(View):
    form_class = CustomRegistrationForm
    template_name = 'accounts/registration.html'  
    success_url = reverse_lazy('profile')

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)        
        if form.is_valid():
            user = form.save()

            authenticated_user = authenticate(email=user.email, password=request.POST['password1'])
            login(request, authenticated_user)

            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, {'form': form})

@method_decorator(user_not_authenticated, name='dispatch')
class CustomLoginView(View):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('profile')

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, {'form': form})

@method_decorator(login_required, name='dispatch')
class CustomProfileView(View):
    template_name = 'accounts/user_profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user  # The logged-in user
        return render(request, self.template_name, {'user': user})

@method_decorator(login_required, name='dispatch')
class CustomPasswordUpdateView(PasswordResetView):
    template_name = 'accounts/password_update.html'

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')  # Redirect to the user's profile or any desired URL
        else:
            messages.error(request, 'Please correct the error below.')

        return render(request, self.template_name, {'form': form})    

@method_decorator(user_not_authenticated, name='dispatch')
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'accounts/password_reset/password_reset.html'
    email_template_name = 'accounts/password_reset/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
 
@method_decorator(login_required, name='dispatch')
class CustomDeleteAccountView(View):
    template_name = 'accounts/delete_account.html'
    success_url = reverse_lazy('login')  # Replace 'home' with your desired URL

    def get(self, request, *args, **kwargs):
        form = DeleteAccountForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = authenticate(request, email=request.user, password=password)

            if user is not None and form.cleaned_data['confirmation']:                
                # Perform account deletion logic here
                request.user.delete()

                # Log the user out
                logout(request)

                return redirect(self.success_url)

        # If password or confirmation checkbox is not valid, show the form again
        form.add_error('password', 'Invalid password or confirmation checkbox not checked.')
        return render(request, self.template_name, {'form': form})


