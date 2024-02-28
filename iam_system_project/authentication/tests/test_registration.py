from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

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

