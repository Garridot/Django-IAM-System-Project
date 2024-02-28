from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm


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

