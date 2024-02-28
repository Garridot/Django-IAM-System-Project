from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.test import Client


from django.core import mail

class CustomRegistrationViewTest(TestCase):
    def setUp(self):
        # Define common user data for registration
        self.user_data = {
            'email': 'testuser@example.com', 
            'password1': 'Testp@ssword123',
            'password2': 'Testp@ssword123',
        }

        # URL for the custom registration view
        self.registration_url = reverse('registration')

    def test_registration_and_redirection(self):
        # Simulate a POST request to the registration view
        response = self.client.post(self.registration_url, data=self.user_data)

        # Check if the user is redirected to the profile page upon successful registration
        self.assertRedirects(response, reverse('profile'))

        # Check if the user is actually registered in the database
        self.assertTrue(get_user_model().objects.filter(email=self.user_data['email']).exists())

        # You can also add additional checks based on your application's logic

    def test_email_failure(self):
        # Simulate a POST request with invalid data to test form validation
        invalid_user_data = self.user_data
        invalid_user_data["email"] = ""

        response = self.client.post(self.registration_url, data=invalid_user_data)
        # Check if the form is not valid and the user is not redirected        
        self.assertContains(response, 'This field is required.')  

    def test_short_password_failure(self):
        # Simulate a POST request with invalid data to test form validation
        invalid_user_data = self.user_data
        invalid_user_data["password1"] = "12345"
        invalid_user_data["password2"] = "12345"        

        response = self.client.post(self.registration_url, data=invalid_user_data)        
        
        # Check if the form is not valid and the expected password error message is present
        self.assertContains(response, 'Your password must contain at least 10 characters.')  

    def test_too_common_password_failure(self):
        # Simulate a POST request with invalid data to test form validation
        invalid_user_data = self.user_data
        invalid_user_data["password1"] = "password"
        invalid_user_data["password2"] = "password"        

        response = self.client.post(self.registration_url, data=invalid_user_data)  
        
        expected_error_message = """Your password must contain at least 1 digit, 1 lower case letter, 1 upper case letter, 1 special character, such as ~!@#$%^&*()_+{}":;'[]."""
        # Check if the form is not valid and the expected password error message is present
        self.assertContains(response, expected_error_message, html=True)      


class CustomLoginViewTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user_data = {
            'email': 'testuser@example.com', 
            'password': 'Testp@ssword123',            
        }
        self.user = get_user_model().objects.create_user(**self.user_data)
        self.url = reverse('login')  # Change 'login' to the actual name of your login view

    def test_login_view(self):
        # Ensure the login page is accessible
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Ensure login form submission works
        response = self.client.post(self.url, data=self.user_data, follow=True)
        self.assertEqual(response.status_code, 200)  # Check if the login form was submitted successfully        

        # Check if the user is redirected to the correct URL
        # self.assertRedirects(response, reverse('profile'))

        # Check if the user is not anonymous
        # self.assertNotIsInstance(response.context['user'], AnonymousUser)


class ProfileViewTest(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = get_user_model().objects.create_user(email='testuser@example.com', password='Testp@ssword123')

        # Set up the client
        self.client = Client()

    def test_profile_view_requires_login(self):
        # Ensure that the view requires login
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # Should be redirected to login page

    def test_profile_view_returns_correct_template(self):
        # Log in the user
        self.client.login(email='testuser@example.com', password='Testp@ssword123')

        # Access the profile view
        response = self.client.get(reverse('profile'))

        # Ensure that the view returns the correct template
        self.assertTemplateUsed(response, 'accounts/user_profile.html')  # Updated template name

    def test_profile_view_passes_user_to_context(self):
        # Log in the user
        self.client.login(email='testuser@example.com', password='Testp@ssword123')

        # Access the profile view
        response = self.client.get(reverse('profile'))

        # Ensure that the user is passed to the context
        self.assertEqual(response.context['user'], self.user)

class CustomPasswordUpdateViewTest(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = get_user_model().objects.create_user(email='testuser@example.com', password='Testp@ssword123')

        # Set up the client
        self.client = Client()

    def test_view_requires_login(self):
        # Ensure that the view requires login
        response = self.client.get(reverse('password_update'))
        self.assertEqual(response.status_code, 302)  # Should be redirected to login page

    def test_get_method_returns_correct_template_and_form(self):
        # Log in the user
        self.client.login(email='testuser@example.com', password='Testp@ssword123')

        # Access the password update view using the GET method
        response = self.client.get(reverse('password_update'))

       # Ensure that the view returns the correct template
        self.assertTemplateUsed(response, 'accounts/password_update.html')

        # Ensure that the context contains a PasswordChangeForm
        self.assertIsInstance(response.context['form'], PasswordChangeForm)

    def test_post_method_updates_password_successfully(self):
        # Log in the user
        self.client.login(email='testuser@example.com', password='Testp@ssword123')

        # Access the password update view using the POST method with valid data
        response = self.client.post(reverse('password_update'), data={
            'old_password': 'Testp@ssword123',
            'new_password1': 'newTestp@ssword123',
            'new_password2': 'newTestp@ssword123',
        })

        # Ensure that the password is updated successfully
        self.assertRedirects(response, reverse('profile'))  # Redirect to the user's profile or any desired URL

   
        updated_user = get_user_model().objects.get(email='testuser@example.com')       

        # Debugging: Try to log in with the updated password
        login_successful = self.client.login(email='testuser@example.com', password='newTestp@ssword123')        

        # Verify that the user is still logged in after password change
        self.assertTrue(login_successful)

    def test_post_method_displays_error_on_invalid_data(self):
        # Log in the user
        self.client.login(email='testuser@example.com', password='Testp@ssword123')

        # Access the password update view using the POST method with invalid data
        response = self.client.post(reverse('password_update'), data={
            'old_password': 'Testp@ssword123',
            'new_password1': 'newTestp@ssword123',
            'new_password2': 'invalidTestp@ssword123',  # Mismatched password
        })

        
        # Ensure that the view returns the correct template
        self.assertTemplateUsed(response, 'accounts/password_update.html')

        # Ensure that an error message is displayed
        self.assertContains(response,'The two password fields didn’t match.')

        # Ensure that the context contains a PasswordChangeForm with errors
        self.assertIsInstance(response.context['form'], PasswordChangeForm)
        self.assertTrue(response.context['form'].errors)


class CustomPasswordResetViewTest(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = get_user_model().objects.create_user(email='testuser@example.com', password='Testp@ssword123')

        # Set up the client
        self.client = Client()

    def test_view_render_correct_template(self):
        # Access the password reset view
        response = self.client.get(reverse('password_reset'))

        # Ensure that the view renders the correct template
        self.assertTemplateUsed(response, 'accounts/password_reset/password_reset.html')

    def test_reset_password_sends_email(self):
        # Access the password reset view and submit the form
        response = self.client.post(reverse('password_reset'), {'email': 'testuser@example.com'})

        # Check that the response redirects to the password reset done page
        self.assertRedirects(response, reverse('password_reset_done'))

        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Check the email subject and recipient
        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Password reset on testserver')
        self.assertEqual(email.to, ['testuser@example.com'])

    def test_reset_password_form_invalid_email(self):
        # Access the password reset view with an invalid email
        response = self.client.post(reverse('password_reset'), {'email': 'invalidemail@1234.com'})

        # Check that the response does not redirect
        self.assertEqual(response.status_code, 200)

        # Check that the view renders the correct template
        self.assertTemplateUsed(response, 'accounts/password_reset/password_reset.html')

        # Check for the form error message in the response content
        self.assertContains(response, 'Email address not found.')   
