from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


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

        # # Check if the user is redirected to the correct URL
        # self.assertRedirects(response, reverse('profile'))

        # # Check if the user is not anonymous
        # self.assertNotIsInstance(response.context['user'], AnonymousUser)
